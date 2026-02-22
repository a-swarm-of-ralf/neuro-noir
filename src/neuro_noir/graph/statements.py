from __future__ import annotations

from typing import Any
from neo4j import Driver

from neuro_noir.models.statement import Statement


SCHEMA = """
CREATE CONSTRAINT statement_id_unique IF NOT EXISTS
FOR (s:Statement)
REQUIRE s.statement_id IS UNIQUE;

CREATE INDEX statement_subject_idx IF NOT EXISTS
FOR (s:Statement) ON (s.subject);

CREATE INDEX statement_predicate_idx IF NOT EXISTS
FOR (s:Statement) ON (s.predicate);

CREATE INDEX statement_object_idx IF NOT EXISTS
FOR (s:Statement) ON (s.object);

CREATE VECTOR INDEX statement_name_embedding_vx IF NOT EXISTS
FOR (s:Statement) ON (s.name_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};

CREATE VECTOR INDEX statement_profile_embedding_vx IF NOT EXISTS
FOR (s:Statement) ON (s.profile_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};
"""


UPSERT_STATEMENT = """
MERGE (c:Chunk {chunk_id: $chunk_id})
MERGE (s:Statement {statement_id: $statement_id})
SET
  s.document_id = $document_id,
  s.chunk_id = $chunk_id,
  s.subject = $subject,
  s.predicate = $predicate,
  s.object = $object,
  s.modality = $modality,
  s.sentence = $sentence,
  s.explanation = $explanation,
  s.name_embedding = $name_embedding,
  s.profile_embedding = $profile_embedding
// expand dynamic attributes onto the node (key/value -> node properties)
SET s += $attributes
// (optional) keep track of which dynamic keys were set
SET s.attribute_keys = keys($attributes)
MERGE (c)-[:HAS_STATEMENT]->(s)
RETURN s;
"""


def params(statement: Statement) -> dict:
    return {
        "statement_id": int(statement.id),
        "document_id": statement.document_id,
        "chunk_id": f"{statement.document_id}_{statement.chunk_index}",
        "subject": statement.subject,
        "predicate": statement.predicate,
        "object": statement.object_,
        "modality": statement.modality,
        "sentence": statement.sentence,
        "explanation": statement.explanation,
        "name_embedding": statement.name_embedding,
        "profile_embedding": statement.profile_embedding,
        "attributes": statement.attributes,
    }


def record_to_statement(data: dict[str, Any]) -> Statement:
    """
    Convert a Neo4j data dictionary containing a statement node into a Statement object.
    """
    statement = Statement(
        id=int(data.get("statement_id", 0)),
        document_id=data.get("document_id", ""),
        chunk_index=int(data.get("chunk_id", "0").split("_")[-1]) if data.get("chunk_id") else 0,
        subject=data.get("subject", ""),
        predicate=data.get("predicate", ""),
        object=data.get("object", ""),
        modality=data.get("modality", []),
        sentence=data.get("sentence", ""),
        explanation=data.get("explanation", ""),
        name_embedding=data.get("name_embedding", []),
        profile_embedding=data.get("profile_embedding", []),
    )
    statement.attributes = {k: data[k] for k in data.get('attribute_keys', [])}
    return statement


def store(driver: Driver, statement: Statement):
    """
    Store a statement in the Neo4j database using the provided driver and the UPSERT_STATEMENT Cypher query.
    The function takes a Statement object, converts it to a dictionary, and executes the query to create or update the corresponding node in the database.
    It returns the stored statement as a dictionary if successful, or raises an exception if the operation fails.
    """
    with driver.session() as session:
        session.run(UPSERT_STATEMENT, params(statement))


def store_all(driver, statements: list[Statement]):
    with driver.session() as session:
        for statement in statements:
            session.run(UPSERT_STATEMENT, params(statement)).consume()


FIND_STATEMENT_BY_ID = """
MATCH (s:Statement {statement_id: $statement_id})
RETURN s
"""


VECTOR_SEARCH_BY_NAME = """
CALL db.index.vector.queryNodes($index_name, $k, $embedding)
YIELD node, score
RETURN node AS s, score
ORDER BY score DESC
LIMIT $k
"""

FIND_STATEMENTS_BY_ENTITY = """
MATCH (e:Entity {entity_id: $entity_id})
MATCH (s:Statement)-[r:HAS_SUBJECT|HAS_OBJECT]->(e)
RETURN
  s,
  type(r) AS role
ORDER BY s.statement_id;
"""


def find_by_id(driver: Driver, statement_id: int) -> Statement | None:
    """
    Find a statement in the Neo4j database by its unique identifier using the provided driver and the FIND_STATEMENT_BY_ID Cypher query.
    The function takes a statement_id as input, executes the query to retrieve the corresponding node from the database, and returns it 
    as a Statement object if found, or None if no matching statement is found.
    """
    with driver.session() as session:
        record = session.run(FIND_STATEMENT_BY_ID, {"statement_id": statement_id}).single() 
        if record is None:
            return None
        return record_to_statement(dict(record["s"]))
    

def search(
    driver: Driver,
    embedding: list[float],
    n: int = 10,
    index_name: str = "statement_name_embedding_vx",
) -> list[tuple[Statement, float]]:
    with driver.session() as session:
        results = session.run(VECTOR_SEARCH_BY_NAME, {
            "index_name": index_name,
            "k": n,
            "embedding": embedding
        })

        statements = []
        for record in results:
            statements.append((record_to_statement(dict(record["s"])), record["score"]))
        return statements
    

def search_by_name(
    driver: Driver,
    embedding: list[float],
    n: int = 10,
) -> list[tuple[Statement, float]]:
    return search(driver, embedding, n, index_name="statement_name_embedding_vx")


def search_by_profile(
    driver: Driver,
    embedding: list[float],
    n: int = 10,
) -> list[tuple[Statement, float]]:
    return search(driver, embedding, n, index_name="statement_profile_embedding_vx")


def search_by_entity(
    driver: Driver,
    entity_id: int,
) -> list[tuple[Statement, float]]:
    with driver.session() as session:
        results = session.run(FIND_STATEMENTS_BY_ENTITY, {"entity_id": entity_id})
        statements = []
        for record in results:
            statements.append((record_to_statement(dict(record["s"])), 1.0))  # Assuming score of 1.0 for entity-based search
        return statements