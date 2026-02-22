from neo4j import Driver
from neuro_noir.models.entity import Entity


SCHEMA = """
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (e:Entity)
REQUIRE e.entity_id IS UNIQUE;

CREATE INDEX entity_canonical_name_idx IF NOT EXISTS
FOR (e:Entity) ON (e.canonical_name);

CREATE INDEX entity_type_idx IF NOT EXISTS
FOR (e:Entity) ON (e.type);

CREATE INDEX entity_aliases_idx IF NOT EXISTS
FOR (e:Entity) ON (e.aliases);

CREATE FULLTEXT INDEX entity_text_ft IF NOT EXISTS
FOR (e:Entity)
ON EACH [e.canonical_name, e.description, e.explanation, e.aliases];

CREATE VECTOR INDEX entity_name_embedding_vx IF NOT EXISTS
FOR (e:Entity) ON (e.name_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};

CREATE VECTOR INDEX entity_profile_embedding_vx IF NOT EXISTS
FOR (e:Entity) ON (e.profile_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};
"""


UPSERT_ENTITY = """
MERGE (e:Entity {entity_id: $entity_id})
SET
  e.canonical_name = $canonical_name,
  e.aliases = $aliases,
  e.type = $type,
  e.category = $category,
  e.description = $description,
  e.explanation = $explanation,
  e.name_embedding = $name_embedding,
  e.profile_embedding = $profile_embedding,
  e.subject_statement_ids = $subject_statement_ids,
  e.object_statement_ids = $object_statement_ids
SET e += $attributes
SET e.attribute_keys = keys($attributes)
RETURN e
"""


LINK_SUBJECT = """
MATCH (s:Statement {statement_id: $statement_id})
MATCH (e:Entity {entity_id: $entity_id})
MERGE (s)-[:HAS_SUBJECT]->(e)
RETURN e, s
"""


LINK_OBJECT = """
MATCH (s:Statement {statement_id: $statement_id})
MATCH (e:Entity {entity_id: $entity_id})
MERGE (s)-[:HAS_OBJECT]->(e)
RETURN e, s
"""


VECTOR_SEARCH = """
CALL db.index.vector.queryNodes($index_name, $k, $embedding)
YIELD node, score
RETURN node AS n, score
ORDER BY score DESC
LIMIT $k
"""


def params(entity: Entity) -> dict:
    return {
        "entity_id": int(entity.id),
        "canonical_name": entity.name,
        "aliases": entity.aliases,
        "type": entity.type_,
        "category": entity.category,
        "description": entity.description,
        "explanation": entity.explanation,
        "name_embedding": entity.name_embedding,
        "profile_embedding": entity.profile_embedding,
        "attributes": entity.attributes,
        "subject_statement_ids": [int(sid) for sid in entity.subject_statement_ids],
        "object_statement_ids": [int(oid) for oid in entity.object_statement_ids]
    }


def record_to_entity(record: dict) -> Entity:
    return Entity(
        id=int(record["entity_id"]),
        name=record["canonical_name"],
        aliases=record["aliases"],
        type=record["type"],
        category=record.get("category", ""),
        description=record["description"],
        explanation=record["explanation"],
        name_embedding=record["name_embedding"],
        profile_embedding=record["profile_embedding"],
        attributes={k: record[k] for k in record["attribute_keys"]} if "attribute_keys" in record else {},
        subject_statement_ids=record.get("subject_statement_ids", []),
        object_statement_ids=record.get("object_statement_ids", [])
    )


def store(driver, entity: Entity):
    with driver.session() as session:
        session.run(UPSERT_ENTITY, params(entity)).consume()
        for sid in entity.subject_statement_ids:
            print(f"Linking entity {entity.id} as subject to statement {sid}")
            session.run(LINK_SUBJECT, {"statement_id": int(sid), "entity_id": int(entity.id)}).consume()
        for oid in entity.object_statement_ids:
            print(f"Linking entity {entity.id} as object to statement {oid}")
            session.run(LINK_OBJECT, {"statement_id": int(oid), "entity_id": int(entity.id)}).consume()


def store_all(driver, entities: list[Entity]):
    print(f"Storing {len(entities)} entities in the database...")
    with driver.session() as session:
        for entity in entities:
            print(f". Storing entity {entity.id}")
            print(f". Subject statement IDs: {entity.subject_statement_ids}")
            print(f". Object statement IDs: {entity.object_statement_ids}")
            session.run(UPSERT_ENTITY, params(entity)).consume()
            print(f". Linking statements for entity {entity.id}")
            print(f". Subject statement IDs: {entity.subject_statement_ids}")
            for sid in entity.subject_statement_ids:
                print(f".   Linking entity {entity.id} as subject to statement {sid}")
                session.run(LINK_SUBJECT, {"statement_id": int(sid), "entity_id": int(entity.id)}).consume()
            print(f". Object statement IDs: {entity.object_statement_ids}")
            for oid in entity.object_statement_ids:
                print(f".   Linking entity {entity.id} as object to statement {oid}")
                session.run(LINK_OBJECT, {"statement_id": int(oid), "entity_id": int(entity.id)}).consume()


def search(
    driver: Driver,
    embedding: list[float],
    n: int = 10,
    index_name: str = "entity_name_embedding_vx",
) -> list[tuple[Entity, float]]:
    with driver.session() as session:
        results = session.run(VECTOR_SEARCH, {
            "index_name": index_name,
            "k": n,
            "embedding": embedding
        })

        entities = []
        for record in results:
            entities.append((record_to_entity(dict(record["n"])), record["score"]))
        return entities
    

def search_by_name(
    driver: Driver,
    embedding: list[float],
    n: int = 10,
) -> list[tuple[Entity, float]]:
    return search(driver, embedding, n, index_name="entity_name_embedding_vx")


def search_by_profile(
    driver: Driver,
    embedding: list[float],
    n: int = 10,
) -> list[tuple[Entity, float]]:
    return search(driver, embedding, n, index_name="entity_profile_embedding_vx")