from neuro_noir.models.document import Document


SCHEMA = """
CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (d:Document)
REQUIRE d.document_id IS UNIQUE;

CREATE INDEX document_title_idx IF NOT EXISTS
FOR (d:Document) ON (d.title);
"""


UPSERT_DOCUMENT = """
MERGE (d:Document {document_id: $document_id})
SET
  d.title = $title
RETURN d;
"""


def params(document: Document) -> dict:
    return {
        "document_id": document.id,
        "title": document.title
    }


def store(driver, document: Document):
    with driver.session() as session:
        session.run(UPSERT_DOCUMENT, params(document)).consume()