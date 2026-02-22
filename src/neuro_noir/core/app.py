from typing import Any, Callable
from neuro_noir.core.config import Settings
from neuro_noir.core.db import delete_db, test_db
from neuro_noir.core.store import Store
from neuro_noir.llm.extractor import extractor
from neuro_noir.models.chunk import Chunk
from neuro_noir.models.document import Document
from neuro_noir.datasets import the_adventure_of_retired_colorman, load_dataset
from neuro_noir.core.lm import test_dspy, test_embedding


class Application:
    
    def __init__(self):
        self.cfg = Settings()
        self.store = Store(base_path=self.cfg.DATA_PATH, name_prefix=self.cfg.DATA_NAME_PREFIX)
        self.user = self.store.create_or_recent()
        self.doc = the_adventure_of_retired_colorman()
        self.entities = []
        self.relationships = []

    def load_document(self, key: str) -> Document:
        self.doc = load_dataset(key)
        return self.doc
    
    def load_chunks(self, user: str | None = None) -> list[str]:
        if user is None:
            user = self.user
        return self.store.load_chunks(user)

    def chunk_document(self, func: Callable[[str], list[str]], user: str | None = None) -> list[str]:
        if user is None:
            user = self.user
        text = self.doc.content
        chunks = func(text)
        self.store.save_chunks(user, chunks)
        return chunks
    
    def clear_entities_and_relationships(self) -> None:
        self.entities = []
        self.relationships = []
    
    def register_entities(self, entities: list[str]) -> None:
        self.entities.extend(entities)

    def register_relationships(self, relationships: list[str]) -> None:
        self.relationships.extend(relationships)

    def extract_triples(self, chunks: list[str], limit: int = 2, user: str | None = None, progress: Callable | None = None) -> list[tuple[str, str, str]]:
        if user is None:
            user = self.user
        results = []
        for i, content in enumerate(chunks[:limit]):
            chunk = Chunk(index=i, document_id=self.doc.id, content=content)
            chunk.embed(self.cfg)
            chunk.extract_statements(self.cfg)
            chunk.disambiguate_entities(self.cfg)
            results.append(chunk)
            progress() if progress else None
        return results
    

    def test_db(self) -> tuple[bool, str, str]:
        """
        Test the Neo4j connection by running a simple query.

        Returns:
            bool: True if the connection is successful, False otherwise.
            str: An error message if the connection fails, or a success message if it succeeds.
        """
        return test_db(self.cfg)
    
    def test_lm(self) -> tuple[bool, str, str]:
        """
        Test the language model connection by making a simple API call.

        Returns:
            bool: True if the connection is successful, False otherwise.
            str: An error message if the connection fails, or a success message if it succeeds.
        """
        return test_dspy(self.cfg)
    
    def test_embedding(self) -> tuple[bool, str, str]:
        """
        Test the embedding function by embedding a simple string.

        Returns:
            bool: True if the embedding is successful, False otherwise.
            str: An error message if the embedding fails, or a success message if it succeeds.
        """
        return test_embedding(self.cfg)
    
    def clear_db(self) -> tuple[bool, str, str]:
        """
        Clear the Neo4j database by deleting all nodes and relationships.
        """
        return delete_db(self.cfg)