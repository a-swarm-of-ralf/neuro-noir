import json
from typing import Callable, Self, Type
from pydantic import BaseModel, Field

from neuro_noir.core.config import Settings
from neuro_noir.core.lm import embed_document
from neuro_noir.core.lm import embed_document
from neuro_noir.llm.resolver import resolver
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
        self.embedding = embed_document(cfg, [self.content])[0] if self.content else []
        return self

    def extract_statements(self, cfg: Settings, starting_id: int = 1) -> list[Statement]:
        """
        Extract statements from the chunk content using the provided extractor function and store them in the statements field.
        The extractor function should take a string input and return a list of Statement objects extracted from the text.
        """
        result = extractor(text=self.content)
        for idx, statement_dict in enumerate(result.statements):
            statement = Statement(**statement_dict, id=starting_id + idx, document_id=self.document_id, chunk_index=self.index)
            statement.attributes = {k: v for k, v in statement_dict.items() if k not in {"subject", "predicate", "object", "modality", "sentence", "explanation", "name_embedding", "profile_embedding", "id", "document_id", "chunk_index"}}
            self.statements.append(statement)

        name_strings = [s.name_string() for s in self.statements]

        profile_strings = [s.profile_string() for s in self.statements]
        name_embeddings = embed_document(cfg, name_strings) if name_strings else []
        profile_embeddings = embed_document(cfg, profile_strings) if profile_strings else []
        for statement, name_embedding, profile_embedding in zip(self.statements, name_embeddings, profile_embeddings):
            statement.name_embedding = name_embedding
            statement.profile_embedding = profile_embedding
        return self.statements
    
    def resolve_entities(self, cfg: Settings, entity_types: list[Type[BaseModel]], starting_id: int = 1) -> list[Entity]:
        """
        Resolve entities in the chunk.
        """
        statements = [s.model_dump(include={'id', 'subject', 'predicate', 'object_', 'modality', 'sentence', 'explanation'}) for s in self.statements]
        categories = [ f"Category: {et.__name__}\nDescription: {json.dumps(et.model_json_schema(),indent=2)}" for et in entity_types ] if entity_types else []
        response = resolver(text=self.content, statements=statements, categories=categories)

        for idx, entity_dict in enumerate(response.entities):
            base_fields = {k:v for k, v in entity_dict.items() if k in {"name", "aliases", "type", "category", "description", "explanation", "name_embedding", "profile_embedding", "statement_ids", "subject_statement_ids", "object_statement_ids"}}
            entity = Entity(**base_fields, id=starting_id + idx)
            entity.attributes = {k: v for k, v in entity_dict.items() if k not in {"name", "aliases", "type", "category", "description", "explanation", "name_embedding", "profile_embedding", "id"}}
            self.entities.append(entity)

        name_strings = [e.name_string() for e in self.entities]
        profile_strings = [e.profile_string() for e in self.entities]
        name_embeddings = embed_document(cfg, name_strings) if name_strings else []
        profile_embeddings = embed_document(cfg, profile_strings) if profile_strings else []
        for entity, name_embedding, profile_embedding in zip(self.entities, name_embeddings, profile_embeddings):
            entity.name_embedding = name_embedding
            entity.profile_embedding = profile_embedding
        return self.entities

    def disambiguate_entities(self, cfg: Settings, ) -> Self:
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