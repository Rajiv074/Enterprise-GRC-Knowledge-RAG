from typing import List, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.documents import Document


class EvidenceGrade(BaseModel):
    grade: Literal["good", "weak"] = Field(
        description=(
            "The grade of the evidence, either 'good' or 'weak'. "
            "Good means the evidence is relevant and reliable, "
            "weak means it is not."
        )
    )


class AgentState(TypedDict):
    question: str
    optimisedquestion: str
    current_query: str
    kb_docs: List[Document]
    kb_grade: str
    answer: str
    citations: List[dict]
    isQueryWriter: bool
    retry_count: int