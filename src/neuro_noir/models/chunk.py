from typing import Callable, Self
from pydantic import BaseModel, Field

from neuro_noir.core.config import Settings
from neuro_noir.core.lm import embed_document
from neuro_noir.core.lm import embed_document
from neuro_noir.llm.disambiguator import disambiguator
from neuro_noir.llm.extractor import extractor
from neuro_noir.models.entity import Entity
from neuro_noir.models.relationship import Relationship
from neuro_noir.models.statement import Statement


class Chunk(BaseModel):
    index: int = Field(default=0, description="The index of the chunk within the document. This should be a sequential number starting from 0 for the first chunk, 1 for the second chunk, and so on.")
    document_id: str = Field(default="", description="The ID of the document this chunk belongs to.")
    content: str = Field(default="", description="The text content of the chunk. This should be a portion of the document content, ideally around 800 characters, but can be more or less depending on the structure of the document and the natural breaks in the text.")
    statements: list[Statement] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    embedding: list[float] = Field(default_factory=list, exclude=True, description="An embedding vector for the chunk content. This can be used for chunk linking or clustering based on content similarity.")


    def embed(self, cfg: Settings) -> Self:
        """
        Generate an embedding vector for the chunk content using the provided embedding function and store it in the embedding field.
        The embedding function should take a string input and return a list of floats representing the embedding vector.
        """
        self.embedding = embed_document(cfg, self.content)
        return self

    def extract_statements(self, cfg: Settings) -> Self:
        """
        Extract statements from the chunk content using the provided extractor function and store them in the statements field.
        The extractor function should take a string input and return a list of Statement objects extracted from the text.
        """
        result = extractor(text=self.content)
        self.statements = [Statement(**statement).embed(cfg) for statement in result.statements]
        return self

    def disambiguate_entities(self, cfg: Settings) -> Self:
        """
        Disambiguate entities in the chunk using the provided disambiguation function and update the entities field.
        The disambiguation function should take a list of Entity objects and return a list of disambiguated Entity objects.
        """
        result = disambiguator(statements=self.model_dump_json(exclude={"content", "embedding"}), text=self.content)
        self.entities = [Entity(**entity).embed(cfg) for entity in result.entities]
        return self

    def classify_entities(self, classification_function: Callable) -> None:
        """
        Classify entities in the chunk using the provided classification function and update the entities field.
        The classification function should take a list of Entity objects and return a list of classified Entity objects.
        """
        self.entities = classification_function(self.entities)

    def classify_relationships(self, classification_function: Callable) -> None:
        """
        Classify relationships in the chunk using the provided classification function and update the relationships field.
        The classification function should take a list of Relationship objects and return a list of classified Relationship objects.
        """
        self.relationships = classification_function(self.relationships)