from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LARGE_MODEL_NAME: str = "gpt-5-mini"
    SMALL_MODEL_NAME: str = "gpt-5-nano"
    OPENAI_API_KEY: str = "<YOUR_OPENAI_API_KEY>"

    GOOGLE_APPLICATION_CREDENTIALS: str = "/path/to/your/google-credentials.json"

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j"

    DSPY_MODEL_NAME: str = "gpt-5-mini" 
    DSPY_API_KEY: str | None = "<YOUR_LLM_API_KEY>"  # Optional: use if you want to use OpenAI instead of Google Vertex AI
    DSPY_VERTEX_PROJECT: str | None = None # Optional: "my-gcp-project" use if you want to use Google Vertex AI instead of OpenAI
    DSPY_TEMPERATURE: float = 1.0
    DSPY_MAX_TOKENS: int = 32000
    DSPY_CACHE: bool = True

    GENAI_USE_VERTEX: bool = True  # Set to True if you want to use Google GenAI client with a Vertex AI model
    GENAI_MODEL_NAME: str = "gemini-2.5-pro"  # Required if GENAI_USE_VERTEX is True
    GENAI_VERTEX_PROJECT: str = "semantic-bank"  # Required if GENAI_USE_VERTEX is True

    DATA_PATH: str = "data/students"
    DATA_NAME_PREFIX: str = "student"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
