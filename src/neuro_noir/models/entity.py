from typing import Self
from pydantic import BaseModel, Field

from neuro_noir.core.config import Settings
from neuro_noir.core.lm import embed_document


class Entity(BaseModel):
    id: int = Field(default=0, exclude=True, description="A unique identifier for the entity.")
    name: str = Field(default="", description="Canonical form of the entity. Prefer fully qualified names (e.g. 'Dr. John Watson' instead of 'Watson'). Try to resolve coreferences and use the most specific form of the name possible, for example if the text mentions 'the big cat' and later refers to it as 'the cat' or 'it', the canonical name should be 'big cat'.")
    aliases: list[str] = Field(default_factory=list, description="A list of aliases for the entity. These can be different forms of the name, pronouns, or other references to the same entity. For example, for the entity 'big cat', the aliases could be ['the big cat', 'the cat', 'it']. For the entity 'She', the aliases could be ['the woman', 'Marta', 'the person'].")
    type_: str = Field(default="", alias="type", description="The type or category of the entity based on the context in which it appears in the text. This should be a concise label that describes what kind of entity it is, such as 'person', 'organization', 'location', 'object', etc.")
    category: str = Field(default="", description="The category of the entity based on the context in which it appears in the text. based on the list of posible categories provided in the input.")
    description: str = Field(default="", description="A brief description of the entity based on the context in which it appears in the text. This should be a concise summary of who or what the entity is, based on the information provided in the text.")
    explanation: str = Field(default="", description="An explanation of how the entity was identified and why the name and aliases were chosen. This should include any reasoning or evidence from the text that supports the identification of the entity and the choice of its canonical name and aliases.")
    name_embedding: list[float] | None = Field(default_factory=list, exclude=True, description="An embedding vector for the entity name. This can be used for entity linking or clustering based on name similarity.")
    profile_embedding: list[float] | None = Field(default_factory=list, exclude=True, description="An embedding vector for the entity profile, which can be derived from the statements and relationships associated with the entity. This can be used for entity linking or clustering based on profile similarity.")
    attributes: dict[str, str] = Field(default_factory=dict, exclude=True, description="A dictionary of additional attributes.")
    subject_statement_ids: list[int] = Field(default_factory=list, exclude=True, description="A list of statement IDs where the entity is the subject.")
    object_statement_ids: list[int] = Field(default_factory=list, exclude=True, description="A list of statement IDs where the entity is the object.")
    

    def name_string(self) -> str:
        """
        Generate a name string for the entity by concatenating the canonical name and aliases with spaces in between.
        This can be used as a canonical name for the entity in the graph database.
        """
        return self.name + " " + " ".join(self.aliases)
    
    def profile_string(self) -> str:
        """
        Generate a profile string for the entity by concatenating the canonical name, aliases, description and explanation with spaces in between.
        This can be used as a more detailed representation of the entity for embedding and similarity comparisons.
        """
        return self.name + " " + " ".join(self.aliases) + " " + self.description + " " + self.explanation
    
    def embed(self, cfg: Settings) -> Self:
        """
        Generate embedding vectors for the entity name and profile using the provided embedding function and store them in the name_embedding and profile_embedding fields.
        The embedding function should take a string input and return a list of floats representing the embedding vector.
        """
        if self.name:
            self.name_embedding = embed_document(cfg=cfg, contents=self.name_string())[0]
        if self.name or self.aliases or self.description or self.explanation:
            self.profile_embedding = embed_document(cfg=cfg, contents=self.profile_string())[0]
        return self