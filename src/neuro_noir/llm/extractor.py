from dspy import Signature, InputField, OutputField, ChainOfThought
from neuro_noir.models.statement import Statement


STATEMENTS_SCHEMA = {
        "type": "array",
        "description": "A list of extracted RDF-like statements (subject–predicate–object) with modality, sentence and explanation.",
        "items": Statement.model_json_schema()
    }


class ExtractStatements(Signature):
        """
        Examine the text and extract ALL core RDF-like statements (subject, predicate, object).

        Instructions
        ------------
        1. Examine the text sentence be sentence
        2. Of each sentence extract all statements. If subject or object contain conjunction create a statement for each option.
        3. Use the pure root of the verb with proposition as predicate.
        4. Based on the intent of the statement add one or more modality to the statement. The modality can be one or more of the following:
            - 'assertion' if this is a statement that is factual or true.
            - 'negation' if this is a statement that is false.
            - 'possibility' if this is a statement that is possible but not certain.
            - 'speculation' if this is a statement that is speculative or hypothetical.
            - 'question' if this is a statement that is a question.
            - 'hypothetical' if this is a statement that is hypothetical or conditional.
            - 'contradiction' if this is a statement that contradicts another statement.
            - 'future' if this is a statement about the future.
            - 'past' if this is a statement about the past.
            - 'present' if this is a statement about the present.
            - Add other modality as needed, but be careful to not add too many modality that are not relevant or useful for understanding the statement.
            - Note that a statement can have multiple modality. For example, if the statement is 'The cat might not be on the mat', the modality would be 'possibility' and 'negation'.
        5. Add an explanation about why the subject, predicate, and object were chooses and why it has that modality.

        Return a JSON array where each item is one statement with metadata.
        """
        text: str = InputField(desc="The text to extract statements from.")

        statements: list = OutputField(
            desc="JSON array of {subject, predicate, object, modality, sentence, explanation}",
            json_schema=STATEMENTS_SCHEMA
        )



extractor = ChainOfThought(ExtractStatements)