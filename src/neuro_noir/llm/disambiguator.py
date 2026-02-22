from dspy import Signature, InputField, OutputField, ChainOfThought
from neuro_noir.models.entity import Entity


ENTITIES_SCHEMA = {
        "type": "array",
        "description": "A list of extracted entities with their aliases and descriptions.",
        "items": Entity.model_json_schema()
    }


class DisambiguateEntities(Signature):
        """
        Examine the statements and classify the entities mentioned in them. For each entity, provide a 
        canonical name, a list of aliases, a brief description based on the context in which it appears 
        in the statements, and an explanation of how the entity was identified and why the name and 
        aliases were chosen.

        Disambiguate entities and resolve coreferences. For example, if the statements mention 'the big cat' 
        and later refer to it as 'the cat' or 'it', the canonical name should be 'big cat' and the aliases 
        should include 'the big cat', 'the cat', and 'it'.

        Be very carefull to fully merge all references to the same entity into a single entity with a 
        canonical name and a list of aliases.

        Instructions
        ------------
        1. Examine the statements and identify all unique entities mentioned in them.
        2. For each entity, determine a canonical name that is the most specific and informative name for the 
           entity based on the context in which it appears in the statements. Prefer fully qualified names 
           (e.g. 'Dr. John Watson' instead of 'Watson').
        3. Carefully resolve coreferences and disambiguate entities. For example, if the statements mention 
           'the big cat' and later refer to it as 'the cat' or 'it', the canonical name should be 'big cat' 
           and the aliases should include 'the big cat', 'the cat', and 'it'.
        3. For each entity, identify a list of aliases that are different forms of the name, pronouns, or other 
           references to the same entity based on the context in which it appears in the statements.
        4. For each entity, write a brief description of who or what the entity is based on the information 
           provided in the statements.
        5. For each entity, write an explanation of how the entity was identified and why the name and aliases 
           were chosen. This should include any reasoning or evidence from the statements that supports the 
           identification of the entity and the choice of its canonical name and aliases.
        
        Return a JSON array where each item is one entity with its canonical name, aliases, description, and explanation.
        """
        text: str = InputField(desc="The text the statements are extracted from. This can be used to provide additional context for entity classification.")
        statements: str = InputField(desc="The statements to classify entities from. This should be a JSON array of {subject, predicate, object, modality, sentence, explanation}.")

        entities: list = OutputField(
            desc="JSON array of {canonical_name, aliases, description, explanation}",
            json_schema=ENTITIES_SCHEMA
        )



disambiguator = ChainOfThought(DisambiguateEntities)