import dspy


class TripleJudge(dspy.Signature):
    """
    Judge the quality of detective-style triples extracted from a paragraph.

    Inputs:
      - history: previous paragraphs or context
      - paragraph: the current paragraph to annotate
      - annotations: list of candidate triples produced by another model,
        each of the form:
        {
          "subject": { "text": str, "type": <EntityType> },
          "relation": <RelationType>,
          "object": { "text": str, "type": <EntityType> },
          "category": <EvidenceCategory>,
          "reasoning": str
        }

    You MUST:
      - Read the paragraph and history carefully.
      - Evaluate whether each triple is:
          * grounded in the text (no hallucinations),
          * using valid entity types and relation types,
          * relevant to detective reasoning
            (e.g., motive, means, opportunity, alibi, testimony, facts).
      - Entitypes: Person, Statement, Location, Event, Object, Evidence, Organization
      - RelationTypes: said, testified, denied, responded_to, refers_to,
        motive_for, has_alibi_for, used_as_means, has_opportunity_for,
        present_at, suspected_of, evidence_of, describes, visited
      - Categories: Fact, Motive, Means, Opportunity, Alibi, Testimony, Identity, Event, Evidence

    Output:
      - score: a float between 0.0 and 1.0 where:
          * 1.0 = all triples are correct, grounded, and useful.
          * 0.0 = triples are mostly wrong, hallucinated, or off-topic.
      - feedback: short textual critique with:
          * what is correct,
          * what is missing or wrong,
          * how to improve future extractions.
    """

    history: list[str] = dspy.InputField()
    paragraph: str = dspy.InputField()
    annotations: list[dict] = dspy.InputField()

    score: float = dspy.OutputField()
    feedback: str = dspy.OutputField()
