from functools import lru_cache

from graphiti_core import Graphiti
from neo4j import GraphDatabase
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.llm_client.config import LLMConfig
from neuro_noir.core.config import Settings
import dspy




@lru_cache(maxsize=1)
def connect_neo4j_cached(uri: str, user: str, pwd: str):
    return GraphDatabase.driver(uri, auth=(user, pwd))


@lru_cache(maxsize=1)
def connect_dspy_large_cached(model: str, key: str):
    lm = dspy.LM(f"openai/{model}", api_key=key, temperature=1.0, max_tokens=32000)
    dspy.configure(lm=lm)
    return lm


@lru_cache(maxsize=1)
def connect_dspy_small_cached(model: str, key: str):
    lm = dspy.LM(f"openai/{model}", api_key=key, temperature=1.0, max_tokens=32000)
    return lm


def connect_neo4j(cfg: Settings):     
    return connect_neo4j_cached(cfg.NEO4J_URI, cfg.NEO4J_USERNAME, cfg.NEO4J_PASSWORD)


def connect_dspy_large(cfg: Settings):
    return connect_dspy_large_cached(cfg.LARGE_MODEL_NAME, cfg.OPENAI_API_KEY)


def connect_dspy_small(cfg: Settings):
    return connect_dspy_small_cached(cfg.SMALL_MODEL_NAME, cfg.OPENAI_API_KEY)


async def connect_graphiti(cfg: Settings):
    llm_config = LLMConfig(
        api_key=cfg.OPENAI_API_KEY,
        model=cfg.LARGE_MODEL_NAME,
        small_model=cfg.SMALL_MODEL_NAME,
        temperature=1.0,
        max_tokens=120000,
    )
    llm_client = OpenAIClient(config=llm_config)
    graphiti = Graphiti(cfg.NEO4J_URI, cfg.NEO4J_USERNAME, cfg.NEO4J_PASSWORD, llm_client=llm_client)
    await graphiti.build_indices_and_constraints()
    return graphiti


def verify_neo4j(cfg: Settings) -> None:
    try:
        driver = connect_neo4j(cfg)
        with driver.session() as session:
            session.run("RETURN 1").consume()
    except Exception as e:
        raise ValueError(f"Failed to connect to Neo4j database: {e}") from e


def verify_dspy(cfg: Settings) -> None:
    large_lm = connect_dspy_large(cfg)
    small_lm = connect_dspy_small(cfg)

    large_response = ["unknown"]
    small_response = ["unknown"]
    try:
        test_prompt = "What is the capital of France?"
        large_response = large_lm(test_prompt)
        small_response = small_lm(test_prompt)
    except Exception as e:
        raise ValueError(f"Failed to verify language models: {e}") from e
    if "Paris" not in large_response[0]:
            raise ValueError(f"Unexpected response from large language model. Expected 'Paris', got '{large_response}'.")
    if "Paris" not in small_response[0]:
        raise ValueError(f"Unexpected response from small language model. Expected 'Paris', got '{small_response}'.")
