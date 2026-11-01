
from itertools import islice
from typing import Iterable, Iterator

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


HUGGINGFACE_EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

EMBEDDING_DIMENSIONS = {
    "sentence-transformers/all-MiniLM-L6-v2": 384,
}

# Cache instances so the model is loaded only once per configuration.
_embeddings_cache: dict[tuple[str, str], HuggingFaceEmbeddings] = {}


def get_embedding_dimension(
    model_name: str = HUGGINGFACE_EMBEDDING_MODEL,
) -> int:
    """Return the known vector dimension for a supported model."""

    if model_name not in EMBEDDING_DIMENSIONS:
        raise ValueError(
            f"Unsupported embedding model: {model_name}"
        )

    return EMBEDDING_DIMENSIONS[model_name]


def get_embeddings(
    model_name: str = HUGGINGFACE_EMBEDDING_MODEL,
    device: str = "cpu",
) -> HuggingFaceEmbeddings:
    """Create and cache the Hugging Face embedding model."""

    cache_key = (model_name, device)

    if cache_key not in _embeddings_cache:
        _embeddings_cache[cache_key] = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    return _embeddings_cache[cache_key]


def embed_text(text: str) -> list[float]:
    """Generate an embedding for a single text or query."""

    embeddings = get_embeddings()
    return embeddings.embed_query(text)


def embed_documents(
    chunks: Iterable[Document],
    batch_size: int = 32,
) -> Iterator[tuple[list[Document], list[list[float]]]]:
    """
    Embed chunks in batches.

    Yields:
        (documents_batch, embeddings_batch)

    Both outputs remain aligned by index.
    """

    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero.")

    embeddings = get_embeddings()
    chunk_iterator = iter(chunks)

    while True:
        batch = list(islice(chunk_iterator, batch_size))

        if not batch:
            break

        texts = [chunk.page_content for chunk in batch]

        vectors = embeddings.embed_documents(texts)

        expected_dimension = get_embedding_dimension()

        if any(len(vector) != expected_dimension for vector in vectors):
            raise ValueError(
                "Embedding model returned an unexpected vector dimension."
            )

        yield batch, vectors
