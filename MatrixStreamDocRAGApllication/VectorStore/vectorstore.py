
import os
import time
from functools import lru_cache

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from MatrixStreamDocRAGApllication.Embedding.EmbeddingService import (
    get_embeddings,
    get_embedding_dimension,
)

load_dotenv()

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
   

NAMESPACE = os.getenv("PINECONE_NAMESPACE")


@lru_cache(maxsize=1)
def get_pinecone_client() -> Pinecone:
    api_key = os.getenv("PINECONE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "PINECONE_API_KEY is missing from your .env file."
        )

    return Pinecone(api_key=api_key)

def sanitize_metadata(metadata: dict) -> dict:
    """Remove metadata values that Pinecone does not support."""
    sanitized = {}

    for key, value in metadata.items():
        if value is None:
            continue

        # Convert tuples to lists if needed
        if isinstance(value, tuple):
            value = list(value)

        sanitized[key] = value

    return sanitized

def ensure_index():
    """Create the new index if missing; never delete an existing index."""

    pc = get_pinecone_client()
    expected_dimension = get_embedding_dimension()

    existing_names = {
        item.name for item in pc.list_indexes()
    }

    if INDEX_NAME not in existing_names:
        print(f"Creating Pinecone index: {INDEX_NAME}")

        pc.create_index(
            name=INDEX_NAME,
            dimension=expected_dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )

        while True:
            info = pc.describe_index(INDEX_NAME)
            if info.status.ready:
                break
            time.sleep(1)

        print(f"Index '{INDEX_NAME}' is ready.")

    info = pc.describe_index(INDEX_NAME)

    if not info.status.ready:
        raise RuntimeError(
            f"Pinecone index '{INDEX_NAME}' is not ready."
        )

    actual_dimension = getattr(info, "dimension", None)

    if (
        actual_dimension is not None
        and actual_dimension != expected_dimension
    ):
        raise ValueError(
            f"Index dimension is {actual_dimension}, but the "
            f"embedding model produces {expected_dimension}. "
            "Choose a compatible index; no index was deleted."
        )

    return pc.Index(INDEX_NAME)


@lru_cache(maxsize=1)
def get_vectorstore() -> PineconeVectorStore:
    """Return a reusable LangChain Pinecone vector store."""

    index = ensure_index()

    return PineconeVectorStore(
        index=index,
        embedding=get_embeddings(),
        namespace=NAMESPACE,
    )



def store_chunks(chunks, batch_size: int = 32) -> int:
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero.")

    vectorstore = get_vectorstore()
    batch = []
    total = 0

    for chunk in chunks:
        # Remove unsupported None metadata values
        chunk.metadata = sanitize_metadata(chunk.metadata)

        batch.append(chunk)

        if len(batch) >= batch_size:
            vectorstore.add_documents(documents=batch)
            total += len(batch)
            print(f"Stored {total} chunks.")
            batch = []

    if batch:
        vectorstore.add_documents(documents=batch)
        total += len(batch)
        print(f"Stored {total} chunks.")

    print(f"Finished storing {total} chunks.")
    return total

