import dspy


class DetectiveAnnotate(dspy.Signature):
    """
    Extract detective-style typed triples from a paragraph,
    using history to establish context.

    Each annotation contains:
    - subject: {text, type}
    - relation: string predicate
    - object: {text, type}
    - category: {Fact, Motive, Means, Opportunity, Alibi, Testimony, Event, Identity}
    - reasoning: justification with references to text

    ────────────────────────────────────────────────
    VALID ENTITY TYPES (choose only from below):
      - Person
      - Statement
      - Location
      - Event
      - Object
      - Evidence
      - Organization

    VALID RELATION TYPES (choose only from below):
      - said               (Person → Statement)
      - testified          (Person → Statement)
      - denied             (Person → Statement)
      - responded_to       (Statement → Statement)
      - refers_to          (Statement → Person/Obj/Event)
      - motive_for         (Person → Event)
      - has_alibi_for      (Person → Event)
      - used_as_means      (Object → Event)
      - has_opportunity_for(Person → Event)
      - present_at         (Person → Location/Event)
      - suspected_of       (Person → Event)
      - evidence_of        (Evidence → Event/Fact)
      - describes          (Statement → Event)
      - visited            (Person → Location)

    VALID CATEGORIES (just one per triple):
      - Fact
      - Motive
      - Means
      - Opportunity
      - Alibi
      - Testimony
      - Identity
      - Event
      - Evidence

    The model MUST NOT create new entity/relationship labels.
    ────────────────────────────────────────────────
    """

    history: list[str] = dspy.InputField()
    paragraph: str = dspy.InputField()

    annotations: list[dict] = dspy.OutputField(
        desc="list of typed triples with reasoning and category"
    )
