from pydantic import BaseModel


class Chunk(BaseModel):
    index: int
    document: str
    title: str
    content: str
