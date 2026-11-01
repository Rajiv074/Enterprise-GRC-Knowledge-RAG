from langchain_community.document_loaders import PyMuPDFLoader

from MatrixStreamDocRAGApllication.Parser.DocumentParser import DocumentParser
from MatrixStreamDocRAGApllication.Chunker.StructureAwareChunker import (
    StructureAwareChunker,
)

PDF_PATH = (
    "MatrixStreamDocRAGApllication/datasource/"
    "hipaa-security-rule-updates.pdf"
)

EXPECTED_PHRASES = [
    "Educate and Engage Leadership",
    "Build a Culture of Cyber Hygiene",
    "Shift from Reactive to Proactive Risk Management",
    "Harmonize Compliance Across Frameworks",
    "Prepare for Future Technology Integration",
]


def main():
    loader = PyMuPDFLoader(PDF_PATH)
    documents = loader.load()

    parser = DocumentParser()

    try:
        parsed_blocks = list(parser.parse_documents(documents))
    finally:
        parser.close()

    chunker = StructureAwareChunker(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = list(chunker.create_chunks(parsed_blocks))

    print(f"Total parsed blocks: {len(parsed_blocks)}")
    print(f"Total chunks: {len(chunks)}")

    print("\n--- Planning Section Chunks ---")

    for index, chunk in enumerate(chunks):
        content = chunk.page_content.lower()

        if any(phrase.lower() in content for phrase in EXPECTED_PHRASES):
            print(f"\nCHUNK {index}")
            print(f"Chunk ID: {chunk.metadata.get('chunk_id')}")
            print(f"Section: {chunk.metadata.get('section')}")
            print(f"Subsection: {chunk.metadata.get('subsection')}")
            print(
                f"Pages: {chunk.metadata.get('page_start')} - "
                f"{chunk.metadata.get('page_end')}"
            )
            print("-" * 80)
            print(chunk.page_content)


if __name__ == "__main__":
    main()