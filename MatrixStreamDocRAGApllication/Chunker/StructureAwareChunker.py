from __future__ import annotations
from typing import Iterable, Iterator
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from MatrixStreamDocRAGApllication.Parser.models import DocumentBlock


class StructureAwareChunker:
    """Convert DocumentBlock objects into LangChain Documents for embedding.

    Normal text is flushed at page/heading/table boundaries. Table row breaks
    are preserved, and oversized tables are split at row boundaries. Chunk IDs
    are unique within one create_chunks() run. This class yields lazily.
    """

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200,
                 separators: list[str] | None = None) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")
        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be >= 0 and < chunk_size.")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap,
            separators=separators or ["\n\n", "\n", ". ", " ", ""],
            length_function=len, keep_separator=True,
        )

    def create_chunks(self, blocks: Iterable[DocumentBlock]) -> Iterator[Document]:
        section: str | None = None
        subsection: str | None = None
        buffer: list[DocumentBlock] = []
        current_page = None
        next_id = 0

        for block in blocks:
            if block.block_type in {"header", "footer"}:
                continue

            # Flush at page boundaries so page_start/page_end remain precise.
            if current_page is not None and block.page != current_page and buffer:
                parts = self._split_body(buffer)
                for i, part in enumerate(parts):
                    yield self._make_text_document(part, buffer, section, subsection, next_id + i)
                next_id += len(parts)
                buffer = []
            current_page = block.page

            if block.block_type == "heading":
                if buffer:
                    parts = self._split_body(buffer)
                    for i, part in enumerate(parts):
                        yield self._make_text_document(part, buffer, section, subsection, next_id + i)
                    next_id += len(parts)
                    buffer = []
                title = block.text.strip()
                level = block.metadata.get("heading_level")
                try:
                    level = int(level) if level is not None else (2 if section is None else 3)
                except (TypeError, ValueError):
                    level = 2 if section is None else 3
                if level <= 1:
                    section, subsection = title, None
                elif level == 2:
                    if section is None:
                        section, subsection = title, None
                    else:
                        subsection = title
                else:
                    if section is None:
                        section = title
                    else:
                        subsection = title
                continue

            if block.block_type == "table":
                if buffer:
                    parts = self._split_body(buffer)
                    for i, part in enumerate(parts):
                        yield self._make_text_document(part, buffer, section, subsection, next_id + i)
                    next_id += len(parts)
                    buffer = []
                table_parts = self._split_table(block, section, subsection)
                for i, part in enumerate(table_parts):
                    yield self._make_table_document(block, part, section, subsection, next_id + i, i)
                next_id += len(table_parts)
                continue

            if block.text and block.text.strip():
                buffer.append(block)

        if buffer:
            parts = self._split_body(buffer)
            for i, part in enumerate(parts):
                yield self._make_text_document(part, buffer, section, subsection, next_id + i)

    def _split_body(self, blocks: list[DocumentBlock]) -> list[str]:
        body = "\n\n".join(self._clean_paragraph(b.text) for b in blocks if b.text and b.text.strip())
        return self.text_splitter.split_text(body) if body.strip() else []

    def _make_text_document(self, part: str, blocks: list[DocumentBlock],
                            section: str | None, subsection: str | None,
                            chunk_id: int) -> Document:
        valid = [b for b in blocks if b.text and b.text.strip()]
        pages = [b.page for b in valid]
        return Document(
            page_content=self._add_context(part, section, subsection),
            metadata={
                "chunk_id": f"chunk_{chunk_id}",
                "source": valid[0].metadata.get("source", "") if valid else "",
                "page_start": min(pages) if pages else None,
                "page_end": max(pages) if pages else None,
                "section": section,
                "subsection": subsection,
                "block_types": list(dict.fromkeys(b.block_type for b in valid)),
                "content_type": "text",
            },
        )

    def _split_table(self, block: DocumentBlock, section: str | None,
                     subsection: str | None) -> list[str]:
        rows = [line.strip() for line in block.text.splitlines() if line.strip()]
        if not rows:
            return []
        prefix = self._context_prefix(section, subsection)
        budget = max(1, self.chunk_size - len(prefix) - (2 if prefix else 0))
        if len("\n".join(rows)) <= budget:
            return ["\n".join(rows)]

        header = rows[0]
        parts: list[str] = []
        current: list[str] = []
        for row in rows:
            if current and len("\n".join(current + [row])) > budget:
                parts.append("\n".join(current))
                # Repeat the first row as a header when splitting the table.
                current = [header, row] if row != header else [row]
            else:
                current.append(row)
        if current:
            parts.append("\n".join(current))
        return parts

    def _make_table_document(self, block: DocumentBlock, part: str,
                             section: str | None, subsection: str | None,
                             chunk_id: int, table_part: int) -> Document:
        return Document(
            page_content=self._add_context(part, section, subsection),
            metadata={
                "chunk_id": f"chunk_{chunk_id}",
                "source": block.metadata.get("source", ""),
                "page_start": block.page,
                "page_end": block.page,
                "section": section,
                "subsection": subsection,
                "block_types": ["table"],
                "content_type": "table",
                "table_index": block.metadata.get("table_index"),
                "table_part": table_part,
            },
        )

    @staticmethod
    def _clean_paragraph(text: str) -> str:
        # Collapse line wraps inside a paragraph; separate blocks remain separated.
        return " ".join(line.strip() for line in text.splitlines() if line.strip())

    @staticmethod
    def _context_prefix(section: str | None, subsection: str | None) -> str:
        parts = []
        if section:
            parts.append(f"Section: {section}")
        if subsection:
            parts.append(f"Subsection: {subsection}")
        return "\n\n".join(parts)

    @classmethod
    def _add_context(cls, content: str, section: str | None,
                     subsection: str | None) -> str:
        prefix = cls._context_prefix(section, subsection)
        return f"{prefix}\n\n{content}" if prefix else content
