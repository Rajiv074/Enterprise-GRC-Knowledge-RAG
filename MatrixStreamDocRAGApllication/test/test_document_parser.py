from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader

from MatrixStreamDocRAGApllication.Parser.DocumentParser import DocumentParser

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
    # 1. Load the PDF pages
    loader = PyMuPDFLoader(PDF_PATH)
    documents = loader.load()

    print(f"PDF pages loaded: {len(documents)}")

    # 2. Parse the pages using your DocumentParser
    parser = DocumentParser()

    try:
        parsed_blocks = list(parser.parse_documents(documents))
    finally:
        parser.close()

    print(f"Total parsed blocks: {len(parsed_blocks)}")

    # 3. Combine all parsed block text
    all_text = "\n".join(
        block.text for block in parsed_blocks
    )

    # 4. Check whether the expected recommendations exist
    print("\n--- Checking HIPAA Planning Section ---")

    for phrase in EXPECTED_PHRASES:
        found = phrase.lower() in all_text.lower()

        status = "FOUND" if found else "MISSING"

        print(f"{status}: {phrase}")

    # 5. Print all parsed blocks from PDF page 2
    # PyMuPDFLoader uses zero-based page numbering.
    print("\n--- Parsed Blocks from PDF Page 2 ---")

    for block in parsed_blocks:
        if int(block.page) == 1:
            print(f"\nBlock Type: {block.block_type}")
            print(f"Text: {block.text}")


if __name__ == "__main__":
    main()