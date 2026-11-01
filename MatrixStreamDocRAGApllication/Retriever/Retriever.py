
from typing import Any

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

try:
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain.retrievers.document_compressors import CrossEncoderReranker
except ImportError:
    from langchain_classic.retrievers import ContextualCompressionRetriever
    from langchain_classic.retrievers.document_compressors import (
        CrossEncoderReranker,
    )

from MatrixStreamDocRAGApllication.VectorStore.vectorstore import (
    get_vectorstore,
)


# 1. Retrieve top-k candidates and filter by Pinecone similarity score
class ThresholdPineconeRetriever(BaseRetriever):
    vectorstore: Any
    k: int = 5
    score_threshold: float = 0.3

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:

        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=self.k,
        )
        print(f"raw result {results}")
        filtered_docs = []

        for doc, score in results:
            # For a cosine index, Pinecone's raw score is a
            # similarity score: higher is more similar.
            if score >= self.score_threshold:
                doc.metadata["pinecone_similarity_score"] = float(score)
                filtered_docs.append(doc)

        print(
            f"Pinecone returned {len(results)} candidates; "
            f"{len(filtered_docs)} passed threshold "
            f"{self.score_threshold}."
        )

        return filtered_docs


# 2. Get your existing Pinecone vector store
vectorstore = get_vectorstore()


# 3. Configure initial retrieval: top 5, minimum score 0.3
similarity_retriever = ThresholdPineconeRetriever(
    vectorstore=vectorstore,
    k=5,
    score_threshold=0.3,
)


# 4. Configure the Hugging Face cross-encoder reranker
cross_encoder = HuggingFaceCrossEncoder(
    model_name="BAAI/bge-reranker-large",
    model_kwargs={"device": "cpu"},
)

reranker = CrossEncoderReranker(
    model=cross_encoder,
    top_n=3,
)


# 5. Final retriever: threshold filter + reranking
final_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=similarity_retriever,
)


def retrieve_documents(query: str) -> list[Document]:
    """Retrieve, threshold-filter, and rerank relevant chunks."""
    return final_retriever.invoke(query)
