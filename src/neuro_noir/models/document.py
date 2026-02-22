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

    def chunks_per_paragraph(self, chunk_size: int = 800, min_chunk_size: int = 100) -> list[str]:
        chunks = []
        active = ""
        for paragraph in self.paragraphs:
            if len(active) + len(paragraph) <= chunk_size:
                # If adding the paragraph doesn't exceed the chunk size, add it to the active chunk
                active += "\n\n" + paragraph if active else paragraph
            elif len(active) < min_chunk_size:
                # If active is too small, we don't want to break it up
                active += "\n\n" + paragraph if active else paragraph
            else:
                # If adding the paragraph exceeds the chunk size, save the active chunk and start a new one
                if active:
                    # Only save the active chunk if it's not empty
                    # This could happen if the first paragraph is larger than the chunk size, in which case 
                    # we want to save it as its own chunk
                    chunks.append(active.strip())
                active = paragraph
        # Don't forget to add the last active chunk if it's not empty
        # The last chunk might not have been added if we reached the end of the paragraphs without exceeding 
        # the chunk size
        # Also, the last chunk can be smaller than the min_chunk_size, but that's okay since it's the last chunk
        if active:
            chunks.append(active.strip())
        return chunks
