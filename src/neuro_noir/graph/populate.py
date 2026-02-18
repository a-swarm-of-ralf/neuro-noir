from dataclasses import dataclass, field
import json
import os
from typing import Optional
import uuid
from zipfile import Path
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError


@dataclass
class EntityNode:
    text: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {"text": self.text, "id": self.id}

@dataclass
class StatementNode:
    predicate: str
    modality: str
    sentence: str
    explanation: str
    embedding: Optional[list[float]] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "predicate": self.predicate,
            "modality": self.modality,
            "sentence": self.sentence,
            "explanation": self.explanation,
        }
        if self.embedding is not None:
            data["embedding"] = self.embedding
        return data

@dataclass
class ChunkNode:
    text: str
    index: int
    embedding: Optional[list[float]] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        data = {
            "text": self.text,
            "index": self.index,
            "id": self.id,
        }
        if self.embedding is not None:
            data["embedding"] = self.embedding
        return data

@dataclass
class DocumentNode:
    title: str
    key: str
    purpose: Optional[str] = None
    audience: Optional[str] = None
    summary: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        data = {
            "title": self.title,
            "key": self.key,
            "id": self.id,
        }
        if self.purpose is not None:
            data["purpose"] = self.purpose
        if self.audience is not None:
            data["audience"] = self.audience
        if self.summary is not None:
            data["summary"] = self.summary
        return data
    


class GraphClient:
    ENTITY = "Entity"
    STATEMENT = "Statement"
    CHUNK = "Chunk"
    DOCUMENT = "Document"
    HAS_CHUNK = "HAS_CHUNK"
    MENTIONS = "MENTIONS"
    SUBJECT = "SUBJECT"
    OBJECT = "OBJECT"

    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        )
        with self.driver.session(database=self.database) as session:
            session.run("RETURN 1")

    def disconnect(self):
        if self.driver:
            self.driver.close()

    def initialize_schema(self):
        if not self.driver:
            raise RuntimeError("Not connected to database")

        constraints = [
            f"CREATE CONSTRAINT IF NOT EXISTS FOR (e:{self.ENTITY}) REQUIRE e.id IS UNIQUE",
            f"CREATE CONSTRAINT IF NOT EXISTS FOR (s:{self.STATEMENT}) REQUIRE s.id IS UNIQUE",
            f"CREATE CONSTRAINT IF NOT EXISTS FOR (c:{self.CHUNK}) REQUIRE c.id IS UNIQUE",
            f"CREATE CONSTRAINT IF NOT EXISTS FOR (d:{self.DOCUMENT}) REQUIRE d.id IS UNIQUE",
            f"CREATE CONSTRAINT IF NOT EXISTS FOR (d:{self.DOCUMENT}) REQUIRE d.key IS UNIQUE",
            f"CREATE INDEX IF NOT EXISTS FOR (e:{self.ENTITY}) ON (e.text)",
            f"CREATE INDEX IF NOT EXISTS FOR (d:{self.DOCUMENT}) ON (d.key)",
        ]

        with self.driver.session(database=self.database) as session:
            for cypher in constraints:
                try:
                    session.run(cypher)
                except Neo4jError:
                    pass

    def create_document(self, doc) -> str:
        if not self.driver:
            raise RuntimeError("Not connected to database")

        query = f"CREATE (d:{self.DOCUMENT} $props) RETURN d.id AS id"

        with self.driver.session(database=self.database) as session:
            result = session.run(query, props=doc.to_dict())
            return result.single()["id"]

    def create_chunk(self, chunk, document_id: str) -> str:
        if not self.driver:
            raise RuntimeError("Not connected to database")

        query = f"""
        MATCH (d:{self.DOCUMENT} {{id: $doc_id}})
        CREATE (c:{self.CHUNK} $chunk_props)
        CREATE (d)-[:{self.HAS_CHUNK}]->(c)
        RETURN c.id AS id
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(query, doc_id=document_id, chunk_props=chunk.to_dict())
            return result.single()["id"]

    def create_statement_with_entities(self, statement, chunk_id: str, subject_text: str, object_text: str) -> str:
        if not self.driver:
            raise RuntimeError("Not connected to database")

        query = f"""
        MATCH (c:{self.CHUNK} {{id: $chunk_id}})
        MERGE (subj:{self.ENTITY} {{text: $subject_text}})
        ON CREATE SET subj.id = randomUUID()
        MERGE (obj:{self.ENTITY} {{text: $object_text}})
        ON CREATE SET obj.id = randomUUID()
        CREATE (s:{self.STATEMENT} $stmt_props)
        CREATE (c)-[:{self.MENTIONS}]->(s)
        CREATE (s)-[:{self.SUBJECT}]->(subj)
        CREATE (s)-[:{self.OBJECT}]->(obj)
        RETURN s.id AS id
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                chunk_id=chunk_id,
                stmt_props=statement.to_dict(),
                subject_text=subject_text,
                object_text=object_text
            )
            return result.single()["id"]

    def document_exists_by_key(self, doc_key: str) -> bool:
        if not self.driver:
            raise RuntimeError("Not connected to database")

        query = f"MATCH (d:{self.DOCUMENT} {{key: $doc_key}}) RETURN d.id"

        with self.driver.session(database=self.database) as session:
            result = session.run(query, doc_key=doc_key)
            return result.single() is not None
        


uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password123")

client = GraphClient(uri, username, password)

client.connect()
print("Connected to Neo4j")

client.initialize_schema()
print("Schema initialized")


docs_dir = Path("./data/documents")

for doc_folder in sorted(docs_dir.iterdir()):
    if not doc_folder.is_dir():
        continue

    doc_name = doc_folder.name

    if client.document_exists_by_key(doc_name):
        print(f"Skipping: {doc_name} (already exists)")
        continue

    print(f"\nProcessing: {doc_name}")

    # Load description for metadata
    description_file = doc_folder / "description.json"
    title = doc_name
    purpose = "AI Risk Management"
    audience = "Organizations"
    summary = "Document for AI governance"
    if description_file.exists():
        try:
            with open(description_file) as f:
                desc_data = json.load(f)
                title = desc_data.get("title", title)
                purpose = desc_data.get("purpose", purpose)
                audience = desc_data.get("audience", audience)
                summary = desc_data.get("summary", summary)
        except Exception as e:
            print(f"  Warning: Could not read description.json: {e}")

    doc = DocumentNode(
        title=title,
        key=doc_name,
        purpose=purpose,
        audience=audience,
        summary=summary
    )
    doc_id = client.create_document(doc)
    print(f"  Created document: {doc_id}")

    # Process chunks
    chunks_file = doc_folder / "chunks.json"
    if chunks_file.exists():
        with open(chunks_file) as f:
            chunks_data = json.load(f)

        for idx, chunk_text in enumerate(chunks_data):
            chunk = ChunkNode(
                text=chunk_text[:1000],
                index=idx
            )
            chunk_id = client.create_chunk(chunk, doc_id)
            print(f"  Created chunk {idx}")

            # Prefer statements with embeddings, fallback to regular statements
            statements_with_embed_file = doc_folder / f"statements-for-chunk-with-embedding-{idx}.json"
            statements_file = doc_folder / f"statements-for-chunk-{idx}.json"

            stmt_file_to_use = None
            if statements_with_embed_file.exists():
                stmt_file_to_use = statements_with_embed_file
            elif statements_file.exists():
                stmt_file_to_use = statements_file

            if stmt_file_to_use:
                try:
                    with open(stmt_file_to_use) as f:
                        stmt_file_data = json.load(f)

                    statements_list = stmt_file_data.get("statements", [])
                    for stmt_data in statements_list:
                        subject_text = stmt_data.get("subject", "")
                        object_text = stmt_data.get("object", "")
                        if not subject_text or not object_text:
                            continue
                        statement = StatementNode(
                            predicate=stmt_data.get("predicate", ""),
                            modality=stmt_data.get("modality", ""),
                            sentence=stmt_data.get("sentence", ""),
                            explanation=stmt_data.get("explanation", ""),
                            embedding=stmt_data.get("embedding")
                        )
                        client.create_statement_with_entities(statement, chunk_id, subject_text, object_text)
                    if statements_list:
                        print(f"    Created {len(statements_list)} statements")
                except Exception as e:
                    print(f"    Warning: Could not process statements: {e}")

print("\nPopulation complete")