from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LARGE_MODEL_NAME: str = "gpt-5-mini"
    SMALL_MODEL_NAME: str = "gpt-5-nano"
    OPENAI_API_KEY: str = "<YOUR_OPENAI_API_KEY>"

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
