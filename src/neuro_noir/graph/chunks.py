from neo4j import Driver
from neuro_noir.models.chunk import Chunk


SCHEMA = """
CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS
FOR (c:Chunk)
REQUIRE c.chunk_id IS UNIQUE;

CREATE INDEX chunk_document_id_idx IF NOT EXISTS
FOR (c:Chunk) ON (c.document_id);

CREATE INDEX chunk_index_idx IF NOT EXISTS
FOR (c:Chunk) ON (c.index);

CREATE FULLTEXT INDEX chunk_content_ft IF NOT EXISTS
FOR (c:Chunk)
ON EACH [c.content];

CREATE VECTOR INDEX chunk_embedding_vx IF NOT EXISTS
FOR (c:Chunk) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};
"""

UPSERT_CHUNK = """
MERGE (d:Document {document_id: $document_id})
MERGE (c:Chunk {chunk_id: $chunk_id})
SET
  c.document_id = $document_id,
  c.index = $index,
  c.content = $content,
  c.embedding = $embedding
MERGE (d)-[:HAS_CHUNK]->(c)
RETURN c;
"""

VECTOR_SEARCH = """
CALL db.index.vector.queryNodes($index_name, $k, $embedding)
YIELD node, score
RETURN node AS c, score
ORDER BY score DESC
LIMIT $k
"""


def params(chunk: Chunk) -> dict:
    return {
        "chunk_id": f"{chunk.document_id}_{chunk.index}",
        "document_id": chunk.document_id,
        "index": chunk.index,
        "content": chunk.content,
        "embedding": chunk.embedding
    }


def record_to_chunk(record: dict) -> Chunk:
    return Chunk(
        document_id=record["document_id"],
        index=record["index"],
        content=record["content"],
        embedding=record["embedding"]
    )


def store(driver, chunk: Chunk):
    with driver.session() as session:
        session.run(UPSERT_CHUNK, params(chunk)).consume()


def store_all(driver, chunks: list[Chunk]):
    with driver.session() as session:
        for chunk in chunks:
            session.run(UPSERT_CHUNK, params(chunk)).consume()


def search(
    driver: Driver,
    embedding: list[float],
    n: int = 10,
) -> list[tuple[Chunk, float]]:
    with driver.session() as session:
        results = session.run(VECTOR_SEARCH, {
            "index_name": "chunk_embedding_vx",
            "k": n,
            "embedding": embedding
        })

        items = []
        for record in results:
            items.append((record_to_chunk(dict(record["c"])), record["score"]))
        return items