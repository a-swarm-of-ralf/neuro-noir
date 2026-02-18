from dspy import Signature, InputField, OutputField, ChainOfThought
from neuro_noir.llm.statement import Statement


STATEMENTS_SCHEMA = {
        "type": "array",
        "description": "A list of extracted RDF-like statements (subject–predicate–object) with deontic modality, sentence and explanation.",
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
        4. Based on the intent of the statement add a modality:
            - 'obligatory' if this is a statement that is required in a project.
            - 'permitted' if this is a statement that is allowed or optional in a project.
            - 'forbidden' if this is a statement that is not allowed in a project.
        5. Add an explanation about why the subject, predicate, and object were chooses and why it has that modality.

        Return a JSON array where each item is one statement with metadata.
        """
        text: str = InputField(desc="The text to extract statements from.")

        statements: list = OutputField(
            desc="JSON array of {subject, predicate, object, modality, sentence, explanation}",
            json_schema=STATEMENTS_SCHEMA
        )



extracter = ChainOfThought(ExtractStatements)