def test_settings():
    from neuro_noir.core.config import Settings
    settings = Settings()
    assert settings.SMALL_MODEL_NAME == "gpt-5-mini"
    assert settings.NEO4J_USERNAME == "neo4j"