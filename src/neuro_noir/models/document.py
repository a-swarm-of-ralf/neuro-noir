from functools import cached_property
from pydantic import BaseModel, computed_field


class Document(BaseModel):
    id: str
    title: str
    content: str

    annotations: list[dict[str, str | list[str] | list[dict[str, str | dict[str, str]]]]] = []

    @computed_field
    @cached_property
    def paragraphs(self) -> list[str]:
        return [paragraph.strip() for paragraph in self.content.split("\n\n") if paragraph.strip()]
    
    @computed_field
    @cached_property
    def chunks(self) -> list[str]:
        return [self.content[i:i+800].strip() for i in range(0, len(self.content), 800) if self.content[i:i+800].strip()]
    
    def rolling_history(self, window: int = 3) -> list[dict[str, list[str] | str]]:
        paragraphs = self.paragraphs
        return [
        {
            "history": paragraphs[max(0, i - window):i],
            "paragraph": paragraphs[i],
        }
        for i in range(len(paragraphs))
    ]
