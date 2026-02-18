from pydantic import BaseModel, Field


class Statement(BaseModel):
        subject: str = Field(..., description="Canonical form of the subject of the statement. Should be single noun or pronoun with at most one adjective.")
        predicate: str = Field(..., description="The root of the verb or predicate of the statement. Use the root of the verb with a possible preposition, but *without* any auxiliary verbs or negations.")
        object_: str = Field(..., alias="object", description="Canonical form of the object of the statement. Should be single noun or pronoun with at most one adjective.")
        modality: str = Field(..., description="The deontic operator or modality of this statement. Must be one of \"obligatory\", \"permitted\", or \"forbidden\".")
        sentence: str = Field(..., description="The sentence from the text the statement appears in.")
        explanation: str = Field(..., description="An explaination of the statement and how the subject, predicate and object were derived from it.")
