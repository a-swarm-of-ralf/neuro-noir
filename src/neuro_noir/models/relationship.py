from typing import Self
from pydantic import BaseModel, Field

from neuro_noir.core.config import Settings
from neuro_noir.core.lm import embed_document


class Relationship(BaseModel):
    name: str = Field(default="", alias="canonical_name", description="Canonical form of the relationship. Prefer fully qualified names (e.g. 'works at' instead of 'works'). Try to resolve coreferences and use the most specific form of the name possible.")
    aliases: list[str] = Field(default_factory=list, description="A list of aliases for the relationship. These can be different forms of the name, tense variations, or synonyms, like 'works at' and 'employed at' could be aliases for the same relationship.")
    description: str = Field(default="", description="A brief description of the relationship based on the context in which it appears in the text. This should be a concise summary of what kind of relationship it is, based on the information provided in the text.")
    explanation: str = Field(default="", description="An explanation of how the relationship was identified and why the name and aliases were chosen. This should include any reasoning or evidence from the text that supports the identification of the relationship and the choice of its canonical name and aliases.")
    name_embedding: list[float] | None = Field(default_factory=list, exclude=True, description="An embedding vector for the relationship name. This can be used for relationship linking or clustering based on name similarity.")
    profile_embedding: list[float] | None = Field(default_factory=list, exclude=True, description="An embedding vector for the relationship profile, which can be derived from the statements and relationships associated with the relationship. This can be used for relationship linking or clustering based on profile similarity.")

    def embed(self, cfg: Settings) -> Self:
        """
        Generate embedding vectors for the relationship name and profile using the provided embedding function and store them in the name_embedding and profile_embedding fields.
        The embedding function should take a string input and return a list of floats representing the embedding vector.
        """
        if self.name:
            self.name_embedding = embed_document(cfg=cfg, content=self.name)
        if self.name or self.aliases or self.description or self.explanation:
            self.profile_embedding = embed_document(cfg=cfg, content=self.name + " " + " ".join(self.aliases) + " " + self.description + " " + self.explanation)
        return self