import synalinks
import os

class Document(synalinks.Entity):
    title: str
    content: str

class Chunk(synalinks.Entity):
    content: str

class IsPartOf(synalinks.Relation):
    source: Chunk
    target: Document

embedding_model = synalinks.EmbeddingModel(
    model="ollama/mxbai-embed-large"
)

knowledge_base = synalinks.KnowledgeBase(
    uri=os.getenv("NEO4J_URI"),
    entity_models=[Document, Chunk],
    relation_models=[IsPartOf],
    embedding_model=embedding_model,
    metric="cosine",
    wipe_on_start=False,
)