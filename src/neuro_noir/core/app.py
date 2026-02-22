from typing import Any, Callable, Type

from pydantic import BaseModel
from neuro_noir import graph
from neuro_noir.core.config import Settings
from neuro_noir.core.db import connect_neo4j, delete_db, test_db
from neuro_noir.core.store import Store
from neuro_noir.graph import chunks, documents, statements, relationships, entities
from neuro_noir.llm.extractor import extractor
from neuro_noir.models.chunk import Chunk
from neuro_noir.models.document import Document
from neuro_noir.datasets import the_adventure_of_retired_colorman, load_dataset
from neuro_noir.core.lm import embed_document, embed_query, test_dspy, test_embedding
from neuro_noir.models.entity import Entity
from neuro_noir.models.statement import Statement


def dummy_progress(increment: int = 1, title: str | None = None, subtitle: str | None = None) -> None:
    """
    A dummy progress function that simulates progress by printing a message to the console.

    Args:
        increment (int): The amount to increment the progress by. This parameter is not used in this dummy function.
        title (str | None): An optional title for the progress. This parameter is not used in this dummy function.
        subtitle (str | None): An optional subtitle for the progress. This parameter is not used in this dummy function.
    """
    print("Progress incremented by", increment)


class Application:
    
    def __init__(self):
        self.cfg = Settings()
        self.store = Store(base_path=self.cfg.DATA_PATH, name_prefix=self.cfg.DATA_NAME_PREFIX)
        self.user = self.store.create_or_recent()
        self.doc = the_adventure_of_retired_colorman()
        self.chunks = []
        self.statements = []
        self.entities = []
        self.relationships = []

        self.entity_types = []
        self.relationship_types = []

    def load_document(self, key: str) -> Document:
        """
        Load a document using the provided key. The key is used to identify which document to load, and the 
        loaded document is stored in the `doc` attribute of the application instance.

        A document is a plain text detective story that will be processed and analyzed in the subsequent steps of 
        the application.

        Args:
            key (str): A string key that identifies the document to be loaded.

        Returns:
            Document: The loaded document object.
        """
        self.doc = load_dataset(key)
        return self.doc
    
    def load_chunks(self, user: str | None = None) -> list[str]:
        if user is None:
            user = self.user
        return self.store.load_chunks(user)

    def chunk_document(self, func: Callable[[str], list[str]], user: str | None = None) -> list[Chunk]:
        print(f"Chunking document {self.doc.id} for user {user}...")
        if user is None:
            user = self.user

        self.clear_db()
        driver = connect_neo4j(self.cfg, cache=False)
        documents.store(driver, self.doc)
        self.chunks = [ Chunk(index=idx + 1, document_id=self.doc.id, content=txt) for idx, txt in enumerate(func(self.doc.content)) if txt.strip() ]
        self.chunks = self.embed_chunks(self.chunks)
        chunks.store_all(driver, self.chunks)
        self.store.store_all(user, "chunk", "json", [m.model_dump_json(include={'index', 'document_id', 'content', 'embedding'}) for m in self.chunks])
        print(f"Chunked document {self.doc.id} into {len(self.chunks)} chunks for user {user}.")
        return self.chunks
    
    def embed_chunks(self, models: list[Chunk]) -> list[Chunk]:
        contents = [chunk.content for chunk in models]
        embeddings = embed_document(self.cfg, contents)
        for chunk, embedding in zip(models, embeddings):
            chunk.embedding = embedding
        return models
    
    def search_chunks(self, query: str, n: int = 5) -> list[tuple[Chunk, float]]:
        driver = connect_neo4j(self.cfg, cache=False)
        query_embedding = embed_query(self.cfg, query)[0]
        results = chunks.search(driver, query_embedding, n=n)
        return results
    
    def clear_entities_and_relationships(self) -> None:
        self.entities = []
        self.relationships = []
        self.entity_types = []
        self.relationship_types = []
    
    def register_entities(self, entities: list[Type[BaseModel]]) -> None:
        self.entity_types.extend(entities)

    def register_relationships(self, relationships: list[Type[BaseModel]]) -> None:
        self.relationship_types.extend(relationships)

    def start_extraction(self) -> None:
        self.statements = []
        
    def do_extraction(self, chunk: Chunk) -> list[Statement]:
        print(f"Extracting statements for chunk {chunk.index} of document {chunk.document_id}...")
        stmts = chunk.extract_statements(self.cfg, starting_id=len(self.statements) + 1)
        self.statements.extend(stmts)
        driver = connect_neo4j(self.cfg, cache=False)
        statements.store_all(driver, stmts)
        self.store.store_all(self.user, "statement", "json", [s.model_dump_json(include={'id', 'document_id', 'chunk_index', 'subject', 'predicate', 'object_', 'modality', 'sentence', 'explanation', 'name_embedding', 'profile_embedding'}, exclude_none=True) for s in stmts])
        return stmts
    
    def end_extraction(self) -> list[Statement]:
        return self.statements
    
    def start_resolution(self) -> None:
        self.entities = []

    def do_resolution(self, chunk: Chunk) -> list[Entity]:
        print(f"Resolving entities for chunk {chunk.index} of document {chunk.document_id}...")
        ents = chunk.resolve_entities(self.cfg, self.entity_types, starting_id=len(self.entities) + 1)
        for entity in ents:
            print(f"Resolved entity {entity.id} with name '{entity.name}' and links to {len(entity.subject_statement_ids)} subject statements and {len(entity.object_statement_ids)} object statements.")
        self.entities.extend(ents)
        print(f"Resolved {len(ents)} entities for chunk {chunk.index} of document {chunk.document_id}.")
        driver = connect_neo4j(self.cfg, cache=False)
        for entity in ents:
            print(f"Storing entity {entity.id} in the database with statement IDs {entity.subject_statement_ids} and {entity.object_statement_ids}")
        entities.store_all(driver, ents)
        print(f"Stored {len(ents)} entities in the database for chunk {chunk.index} of document {chunk.document_id}.")
        self.store.store_all(self.user, "entity", "json", [e.model_dump_json(include={'id', 'name', 'aliases', 'type', 'category', 'description', 'explanation', 'name_embedding', 'profile_embedding', 'statement_ids'}, exclude_none=True) for e in ents])
        return ents

    def end_resolution(self) -> list[Entity]:
        return self.entities

    def process_chunks(self, chunks: list[str], limit: int = 2, user: str | None = None, progress: Callable | None = None, clear_graph: bool = False) -> list[tuple[str, str, str]]:
        if user is None:
            user = self.user
        if clear_graph:
            self.clear_db()
        if progress is None:
            progress = dummy_progress
        results = []
        for i, content in enumerate(chunks[:limit]):
            chunk = Chunk(index=i, document_id=self.doc.id, content=content)
            chunk = self.process_chunk(chunk, user, progress)
            results.append(chunk)
        return results
    
    def process_chunk(self, chunk: Chunk, user: str, progress: Callable) -> Chunk:
        progress(increment=1, title=f"Processing Chunk {chunk.index}", subtitle=f"Starting processing for Chunk {chunk.index} of Document {chunk.document_id}")
        chunk.embed(self.cfg)
        progress(increment=1, title=f"Processing Chunk {chunk.index}", subtitle=f"Embedding Created for Chunk {chunk.index} of Document {chunk.document_id}")
        chunk.extract_statements(self.cfg)
        progress(increment=1, title=f"Processing Chunk {chunk.index}", subtitle=f"{len(chunk.statements)} Statements Extracted for Chunk {chunk.index} of Document {chunk.document_id}")
        chunk.disambiguate_entities(self.cfg)
        progress(increment=1, title=f"Processing Chunk {chunk.index}", subtitle=f"{len(chunk.entities)} Entities Disambiguated for Chunk {chunk.index} of Document {chunk.document_id}")
        return chunk

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