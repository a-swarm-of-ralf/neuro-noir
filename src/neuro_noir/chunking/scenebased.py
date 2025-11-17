import os
import dspy
from pydantic import BaseModel
from neuro_noir.core.config import Settings
from neuro_noir.models.chunk import Chunk
from neuro_noir.models.document import Document

class Scene(BaseModel):
    title: str
    content: str
    
    
class ChunkByScene(dspy.Signature):
    """Split this story into coherent scenes, preserving conversations, location, and context."""
    story: str = dspy.InputField(description="The full text of the document to be chunked.")
    scenes: list[str] = dspy.OutputField(description="A list of coherent text segments.")

class SceneBasedChunker:
    def __init__(self, document: Document, cfg: Settings):
        self.document = document
        self.cfg = cfg
        self.lm = dspy.LM(self.cfg.MODEL_NAME, temperature=1.0, max_tokens=32000)
        if not os.environ['OPENAI_API_KEY']:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        dspy.configure(lm=self.lm)
        self.chunker = dspy.ChainOfThought(ChunkByScene)

    def chunk(self) -> list[Chunk]:
        response = self.chunker(story=self.document.content)
        scenes = response.segements
        return [Chunk(id=f"scene_{i+1}",document_id=self.document.id,title=f"Scene {i+1}",content=scene) for i, scene in enumerate(scenes)]