from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentBlock:

    block_type: str

    text: str

    page: int

    section: str | None = None

    subsection: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )