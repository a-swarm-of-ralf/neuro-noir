from neuro_noir.core.config import Settings
import dspy
from google import genai # type: ignore
from google.genai import types


def connect_dspy(cfg: Settings):
    if cfg.DSPY_MODEL_NAME.startswith("vertex_ai/"):
        lm = dspy.LM(cfg.DSPY_MODEL_NAME, vertex_project=cfg.DSPY_VERTEX_PROJECT, temperature=cfg.DSPY_TEMPERATURE, max_tokens=cfg.DSPY_MAX_TOKENS, cache=cfg.DSPY_CACHE)
    else:
        lm = dspy.LM(cfg.DSPY_MODEL_NAME, api_key=cfg.DSPY_API_KEY, temperature=cfg.DSPY_TEMPERATURE, max_tokens=cfg.DSPY_MAX_TOKENS, cache=cfg.DSPY_CACHE)
    dspy.configure(lm=lm)
    return lm


def test_dspy(cfg: Settings) -> tuple[bool, str, str]:
    """
    Test the dspy connection by making a simple API call.

    Returns:
        bool: True if the connection is successful, False otherwise.
        str: An error message if the connection fails, or a success message if it succeeds.
    """
    try:
        lm = connect_dspy(cfg)
        # Make a simple API call to generate text
        response = lm("Answer with 'Connected to dspy successfully.'")
        return True, f"✅ Completion connection successful.", f"dspy connection successful. Response: {response[0]}"
    except Exception as e:
        return False, "", f"dspy connection failed: {str(e)}"


def connect_genai(cfg: Settings):
    return genai.Client(vertexai=cfg.GENAI_USE_VERTEX, project=cfg.GENAI_VERTEX_PROJECT)
    

def embed(cfg: Settings, contents: str | list[str], task_type: str = "RETRIEVAL_QUERY") -> list[list[float]]:
    client = connect_genai(cfg)
    response = client.models.embed_content(
        model='gemini-embedding-001',
        contents=contents,  
        config=types.EmbedContentConfig(task_type=task_type, output_dimensionality=1536)
    )
    return [emb.values for emb in response.embeddings] if response.embeddings else []
    

def embed_query(cfg: Settings, contents: str | list[str]) -> list[list[float]]:
    contents = [contents] if isinstance(contents, str) else contents
    return embed(cfg, contents, task_type="RETRIEVAL_QUERY")


def embed_document(cfg: Settings, contents: str | list[str]) -> list[list[float]]:
    contents = [contents] if isinstance(contents, str) else contents
    return embed(cfg, contents, task_type="RETRIEVAL_DOCUMENT")


def test_embedding(cfg: Settings) -> tuple[bool, str, str]:
    """
    Test the embedding function by embedding a simple string.

    Returns:
        bool: True if the embedding is successful, False otherwise.
        str: An error message if the embedding fails, or a success message if it succeeds.
    """
    try:
        embedding = embed(cfg, "Test embedding")
        if embedding and len(embedding) > 0:
            return True, f"✅ Embedding successful. Embedding length: {len(embedding)}", ""
        else:
            return False, "❌ Embedding failed. No values returned.", ""
    except Exception as e:
        return False, "", f"Embedding failed: {str(e)}"