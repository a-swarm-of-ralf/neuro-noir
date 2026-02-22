from dspy import Signature, InputField, OutputField, ChainOfThought
from neuro_noir.models.entity import Entity
from neuro_noir.models.statement import Statement


STATEMENTS_SCHEMA = {
        "type": "array",
        "description": "A list of extracted RDF-like statements (subject–predicate–object) with modality, sentence and explanation.",
        "items": Statement.model_json_schema()
    }

ENTITIES_SCHEMA = {
        "type": "array",
        "description": "A list of extracted entities with their aliases and descriptions.",
        "items": Entity.model_json_schema()
    }


class ResolveEntities(Signature):
        """
        Examine the statements resolve the subjects and objects in them to entities. For each entity, provide a 
        canonical name, a list of aliases, a brief description based on the context in which it appears in the 
        statements, and an explanation of how the entity was identified and why the name and aliases were chosen.

        It is very important to carefully resolve coreferences and disambiguate entities. For example 'You',
        'He', 'She', 'It', are meaningless without context. Prefer fully qualified names that don't require
        context to understand (e.g. 'Dr. John Watson' instead of 'He').

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
        6. And finally, for each entity, provide a list of statement IDs for each statement where the entity is 
           the subject and a list of statement IDs for each statement where the entity is the object. This can 
           be used to link the entity to the statements it appears in.
        
        Return a JSON array where each item is one entity with its 
        - name: str
        - category: str
        - aliases: list[str] 
        - type_: str
        - description: str
        - explanation: str
        - subject_statement_ids: list[int] (a list of statements IDS where the entity is the subject. This can be used to link the entity to the statements it appears in.)
        - object_statement_ids: list[int] (a list of statements IDS where the entity is the object. This can be used to link the entity to the statements it appears in.)

        Categories can request extra fields to be extracted for the entity. For example, a categoy of 'person' could request to extract the person's occupation, date of birth, etc. These extra fields can be added at entity level.
        """
        text: str = InputField(desc="The text the statements are extracted from. This can be used to provide additional context for entity classification.")

        categories: list[str] = InputField(desc="The category of the entities to resolve. This can be used to provide additional context for entity classification and disambiguation. For example, if the category is 'person', the resolver can use this information to prefer person names and pronouns as canonical names for the entities.")

        statements: list = InputField(desc="The statements to resolve entities from.", json_schema=STATEMENTS_SCHEMA)

        entities: list = OutputField(
            desc="JSON array of {canonical_name, aliases, description, explanation}",
            json_schema=ENTITIES_SCHEMA
        )



resolver = ChainOfThought(ResolveEntities)