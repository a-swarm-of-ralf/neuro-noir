from typing import Self
from pydantic import BaseModel, Field

from neuro_noir.core.config import Settings
from neuro_noir.core.lm import embed_document


class Statement(BaseModel):
        id: int = Field(default=0, description="A unique identifier for the statement. Don't Generate.")
        document_id: str = Field(default="", exclude=True, description="The ID of the document this statement belongs to.")
        chunk_index: int = Field(default=0, exclude=True, description="The index of the chunk this statement belongs to.")
        subject: str = Field(default="", description="Canonical form of the subject of the statement. Should be single noun or pronoun with at most one adjective. For example, if the sentence is 'The big cat is on the mat', the subject would be 'big cat'. If the sentence is 'She is happy', the subject would be 'She' but use the actual canonical form to which it refers, for example 'the woman' or 'Marta'if clear form the surrounding context.")
        predicate: str = Field(default="", description="The root of the verb or predicate of the statement. Use the root of the verb with a possible preposition, but *without* any auxiliary verbs or negations.")
        object_: str = Field(default="", alias="object", description="Canonical form of the object of the statement. Should be single noun or pronoun with at most one adjective.")
        modality: list[str] = Field(default_factory=list, description="The modality of the statement, which can be one or more of the following: 'assertion', 'negation', 'possibility', 'speculation', 'question', 'hypothetical', or others. This indicate how the predicate relates the subject and object. For example, if the statement is 'The cat is on the mat', the modality would be 'assertion'. If the statement is 'The cat might be on the mat', the modality would be 'possibility'. If the statement is 'Is the cat on the mat?', the modality would be 'question'.")
        sentence: str = Field(default="", description="The sentence from the text the statement appears in.")
        explanation: str = Field(default="", description="An explanation of the statement and how the subject, predicate and object were derived from it.")
        name_embedding: list[float] | None = Field(default_factory=list, exclude=True, description="An embedding vector for the statement name. This can be used for statement linking or clustering based on name similarity.")
        profile_embedding: list[float] | None = Field(default_factory=list, exclude=True, description="An embedding vector for the statement profile, which can be derived from the statements and relationships associated with the statement. This can be used for statement linking or clustering based on profile similarity.")

        attributes: dict[str, str] = Field(default_factory=dict, exclude=True, description="A dictionary of additional attributes.")
        

        def name_string(self) -> str:
                """
                Generate a name string for the statement by concatenating the subject, predicate and object with spaces in between.
                This can be used as a canonical name for the statement in the graph database.
                """
                return self.subject + " " + self.predicate + " " + self.object_
        
        def profile_string(self) -> str:
                """
                Generate a profile string for the statement by concatenating the subject, predicate, object, modality, sentence and explanation with spaces in between.
                This can be used as a more detailed representation of the statement for embedding and similarity comparisons.
                """
                return self.subject + " " + self.predicate + " " + self.object_ + " " + str(self.modality) + " " + self.sentence + " " + self.explanation
        
        def embed(self, cfg: Settings) -> Self:
                """
                Generate embedding vectors for the statement name and profile using the provided embedding function and store them in the name_embedding and profile_embedding fields.
                The embedding function should take a string input and return a list of floats representing the embedding vector.
                """
                if self.subject or self.predicate or self.object_:
                        self.name_embedding = embed_document(cfg=cfg, contents=self.subject + " " + self.predicate + " " + self.object_)[0]
                if self.subject or self.predicate or self.object_ or self.modality or self.sentence or self.explanation:
                        self.profile_embedding = embed_document(cfg=cfg, contents=self.subject + " " + self.predicate + " " + self.object_ + " " + str(self.modality) + " " + self.sentence + " " + self.explanation)[0]
                return self