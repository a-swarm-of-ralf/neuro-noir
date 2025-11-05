import synalinks
import os

print("Loading model from environment variable OPENAI_MODEL:", os.getenv("OPENAI_MODEL"))
language_model = synalinks.LanguageModel(model=os.getenv("LLM_MODEL"))