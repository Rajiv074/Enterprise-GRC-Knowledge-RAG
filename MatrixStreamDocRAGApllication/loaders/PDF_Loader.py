from pathlib import Path

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyMuPDFLoader,
)


def load_source_document():
    """
    Load all PDF documents from the datasource directory.

    Returns:
        Iterator[Document]: Lazy iterator that yields one
        LangChain Document per PDF page.
    """

    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "datasource"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Datasource directory not found: {data_path}"
        )

    loader = DirectoryLoader(
        str(data_path),
        glob="**/*.pdf",
        loader_cls=PyMuPDFLoader,
        show_progress=True,
    )

    return loader.lazy_load()