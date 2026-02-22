from neuro_noir.models.relationship import Relationship


SCHEMA = """
CREATE CONSTRAINT relationship_id_unique IF NOT EXISTS
FOR (r:Relationship)
REQUIRE r.relationship_id IS UNIQUE;

CREATE INDEX relationship_canonical_name_idx IF NOT EXISTS
FOR (r:Relationship) ON (r.canonical_name);

CREATE INDEX relationship_aliases_idx IF NOT EXISTS
FOR (r:Relationship) ON (r.aliases);

CREATE FULLTEXT INDEX relationship_text_ft IF NOT EXISTS
FOR (r:Relationship)
ON EACH [r.canonical_name, r.description, r.explanation, r.aliases];

CREATE VECTOR INDEX relationship_name_embedding_vx IF NOT EXISTS
FOR (r:Relationship) ON (r.name_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};

CREATE VECTOR INDEX relationship_profile_embedding_vx IF NOT EXISTS
FOR (r:Relationship) ON (r.profile_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};
"""

UPSERT_RELATIONSHIP = """
MERGE (r:Relationship {relationship_id: $relationship_id})
SET
  r.canonical_name = $canonical_name,
  r.aliases = $aliases,
  r.description = $description,
  r.explanation = $explanation,
  r.name_embedding = $name_embedding,
  r.profile_embedding = $profile_embedding
SET r += $attributes
SET r.attribute_keys = keys($attributes)
RETURN r;
"""


def params(relationship: Relationship) -> dict:
    return {
        "relationship_id": relationship.id,
        "canonical_name": relationship.name,
        "aliases": relationship.aliases,
        "description": relationship.description,
        "explanation": relationship.explanation,
        "name_embedding": relationship.name_embedding,
        "profile_embedding": relationship.profile_embedding,
        "attributes": relationship.attributes
    }