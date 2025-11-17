# Workshop Neuro-Noir

An introduction workshop to neurosymbolic AI. In this hands-on session, you’ll build a reasoning agent that doesn’t just *guess* the answer to a mystery, but can **show its work**.

## Why Neurosymbolic AI?

Most modern AI systems are great at pattern-matching: they predict likely answers from vast amounts of data. That’s powerful—but not always trustworthy.

**Neurosymbolic AI** combines two worlds:
- **Neural**: language models for reading, summarizing, extracting clues.
- **Symbolic**: graphs, rules, constraints, and logic for structuring facts and testing hypotheses.

In Neuro-Noir, we use LLMs to parse and interpret text, then store the results in a **knowledge graph** with entities like *Person*, *Location*, *Motive*, *Opportunity*, *Means*, and relationships like *WAS_AT*, *WITNESSED_BY*, *HAS_MOTIVE*, and *CONTRADICTS*.  
On top of that, we add reasoning steps that let the system explain *why* a suspect is innocent or guilty.

## The Mystery You’ll Be Solving

We work with a classic-style detective story:

- Multiple suspects  
- Conflicting statements  
- Timelines, locations, and alibis  
- Motive, means, and opportunity

Instead of “magic black box” answers, you’ll encode:

- Who was where, when.
- Who could realistically have committed the crime.
- How new evidence can *invalidate* previous assumptions (e.g. a broken alibi).

Your agent’s job is not just to pick a culprit, but to navigate these constraints logically and transparently—like a careful investigator, not a psychic.

## What You’ll Learn

By the end of the workshop, you will:

- Understand the **core idea of neurosymbolic AI** and where it fits in real-world use cases.
- Learn how to:
  - Chunk narrative text into meaningful “episodes”.
  - Extract entities, relations, and evidence using an LLM.
  - Store them in a **graph database** (Neo4j + Graphiti).
  - Model concepts like alibis, motives, and contradictions.
- Build a simple **reasoning pipeline** that:
  - Updates beliefs when new evidence appears.
  - Makes its reasoning inspectable (“Why this suspect?” “Why not that one?”).
- See how to move from “LLM as oracle” to **LLM as tool inside a structured reasoning system**.

---

/// details | “But can’t a normal LLM just tell me the culprit?”
    type: info

Yes. And that’s exactly the point.

We intentionally use well-known stories. If you ask a generic LLM directly, “Who did it?”, it will probably answer correctly from training data or pattern matching—**without reading your evidence**, **without using your rules**, and **without explaining its logic in a verifiable way**.

This workshop is about something different:

- **Control**: Use *your* data, *your* rules, *your* constraints.
- **Transparency**: See which facts lead to which conclusions.
- **Robustness**: Handle conflicting statements, retracted alibis, and evolving evidence.
- **Realism**: Mirror how you’d build systems for fraud detection, investigations, audits, compliance, or safety-critical decisions—where “the model just knows” is not good enough.

So yes, an LLM can guess the answer.  
We’re here to learn how to **prove** it.
///
