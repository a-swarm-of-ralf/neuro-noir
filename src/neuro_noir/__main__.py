import asyncio
import synalinks
import dotenv
import os


dotenv.load_dotenv()


class Query(synalinks.DataModel):
    query: str = synalinks.Field(description="The user query")


class AnswerWithThinking(synalinks.DataModel):
    thinking: str = synalinks.Field(description="Your step by step thinking")
    answer: str = synalinks.Field(description="The correct answer")


language_model = synalinks.LanguageModel(model="openai/gpt-5-mini-2025-08-07")


async def main():
    print("Welcome to Neuro Noir!")
    print(f"Synalinks version: {synalinks.__version__}")
    print(f"* Model used: {os.getenv('OPENAI_MODEL')}")
    print(f"* Graph used: {os.getenv('NEO4J_DATABASE')}")
    print(f"* Graph URI: {os.getenv('NEO4J_URI')}")
    synalinks.clear_session()

    inputs = synalinks.Input(data_model=Query)
    outputs = await synalinks.Generator(
        data_model=AnswerWithThinking,
        language_model=language_model,
    )(inputs)

    program = synalinks.Program(
        inputs=inputs,
        outputs=outputs,
        name="chain_of_thought",
        description="Useful to answer in a step by step manner.",
    )


if __name__ == "__main__":
    asyncio.run(main())