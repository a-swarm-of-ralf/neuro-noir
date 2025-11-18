import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Workshop Neuro-Noir

    Step into a world where classic whodunits meet modern AI: in this workshop, you’ll use neurosymbolic techniques to teach machines to reason about suspects, motives, alibis, and contradictions—step by step, and in the open.

    ## Introduction

    In this hands-on session, we move beyond “the model just knows” and focus on **how** an AI arrives at its conclusions. You’ll build a reasoning pipeline that reads a mystery, extracts structured facts, and uses a knowledge graph plus logical rules to evaluate competing hypotheses about who could have done it.


    /// details | Why Neurosymbolic AI?
        type: info

    Most modern AI systems are great at pattern-matching: they predict likely answers from vast amounts of data. That’s powerful—but not always trustworthy.

    **Neurosymbolic AI** combines two worlds:
    - **Neural**: language models for reading, summarizing, extracting clues.
    - **Symbolic**: graphs, rules, constraints, and logic for structuring facts and testing hypotheses.

    In Neuro-Noir, we use LLMs to parse and interpret text, then store the results in a **knowledge graph** with entities like *Person*, *Location*, *Motive*, *Opportunity*, *Means*, and relationships like *WAS_AT*, *WITNESSED_BY*, *HAS_MOTIVE*, and *CONTRADICTS*.
    On top of that, we add reasoning steps that let the system explain *why* a suspect is innocent or guilty.

    ///

    /// details | The Mystery You’ll Be Solving
        type: info

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

    ///

    /// details | What You’ll Learn
        type: info

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

    ///

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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tasks

    ### 1. Select a Case

    Select one of the four cases to use in your workshop.

    ### 2. Create Schema

    Create a schema for the knowledge graph.

    ### 3. Chunk the Text

    Split the story into segments to process.

    ### 4. Create Knowledge Graph

    Run your segements with teh schema to create the knowledge graph.

    ### 5. Enhance Knowledge Base

    Add some logic derivations to the knoweldge graph.

    ### 6. Query the Knowledge Graph

    Query the Knowledge Graph

    ### 7. Create Reasoning Agent

    Create an Agent that can use the Knowledge Graph to reason about the case.
    """)
    return


@app.cell
def _(mo):
    run_test_neo4j = mo.ui.run_button(label="Test Database", kind="info", full_width=True)
    run_test_dspy = mo.ui.run_button(label="Test Language Model", kind="info", full_width=True)
    run_delete_neo4j = mo.ui.run_button(label="💀💀💀Delete Database 💀💀💀", kind="danger", full_width=True)



    mo.md(f"""
    ## Test Settings

    Before running these tests, ensure your environment is configured.

    /// details | Configure your .env
        type: info

    This notebook reads its settings from a .env file at the project root. Copy .env.example to .env and fill in the required keys. The example file shows the exact variable names you need to set, including:
    - Neo4j connection settings (e.g., NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    - LLM provider configuration and API key (e.g., OPENAI_API_KEY or your chosen provider)

    After editing .env, restart the kernel or re-run the setup cells so the changes take effect.
    ///


    We will be using <span data-tooltip="Neo4j is a native graph database that models data as nodes (entities) and relationships (edges), supports the Cypher query language, and excels at traversals, path finding, and knowledge-graph workloads.">Neo4j</span> in this workshop. Press the button below to test the database connection.
    {run_test_neo4j}

    We will be using <span data-tooltip="gpt-5 is an advanced large language model used in this workshop for reading, extraction, and step-by-step reasoning. Ensure your API credentials are configured.">gpt-5</span> for language understanding and extraction. Press the button below to test that your language model is configured and working.
    {run_test_dspy}

    /// admonition | 💀 Danger: Wipes Neo4j Database
        type: danger

    Pressing the button below will permanently DELETE the entire Neo4j database for this workshop — all nodes, relationships, metadata, and embeddings. Use this only if you need to start fresh after making a mess. There is no undo.
    {run_delete_neo4j}
    ///
    """)
    return run_delete_neo4j, run_test_dspy, run_test_neo4j


@app.cell(hide_code=True)
def _(cfg, mo, run_test_neo4j, verify_neo4j):
    if run_test_neo4j.value:
        try:
            verify_neo4j(cfg)
            mo.output.append(mo.md(f"""
    /// details | ✅ Successfully connected to Neo4j
        type: success
    ✅ Yay, it worked. We have a connection!
    ///
            """))
        except Exception as _e:
            mo.output.append(mo.md(f"""
    /// details | ❌ Failed to connect to Neo4j
        type: danger
    ❌ {_e}
    ///
            """))
    return


@app.cell(hide_code=True)
def _(cfg, mo, run_test_dspy, verify_dspy):
    if run_test_dspy.value:
        try:
            verify_dspy(cfg)
            mo.output.append(mo.md(f"""
    /// details | ✅ Successfully connected to LLM
        type: success
    ✅ Yay, it worked. We have a connection!
    ///
            """))
        except Exception as _e:
            mo.output.append(mo.md(f"""
    /// details | ❌ Failed to connect to LLM
        type: danger
    ❌ {_e}
    ///
            """))
    return


@app.cell(hide_code=True)
def _(cfg, mo, run_delete_neo4j, verify_dspy):
    if run_delete_neo4j.value:
        try:
            verify_dspy(cfg)
            mo.output.append(mo.md(f"""
    /// details | ✅  Successfully deleted database
        type: success
    ✅ It's gone, jim!
    ///
            """))
        except Exception as _e:
            mo.output.append(mo.md(f"""
    /// details | ❌ Failed to delete database
        type: danger
    ❌ {_e}
    ///
            """))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Select a Case

    For this workshop, you’ll work with the **raw text** of a classic mystery and turn it into a structured, queryable case.

    You can choose one of the following stories:

    - **The Adventure of the Retired Colourman**
      A suspicious husband, a missing wife, a vanished agent, and a locked strong-room.
      Compact case with clear financial motive, opportunity, and physical evidence — great for beginners.

    - **The Adventure of the Three Students**
      An exam paper is tampered with and three students fall under suspicion.
      Focused on timelines, access control, and subtle behavioral clues — ideal if you like **process** and **constraints**.

    - **The Five Orange Pips**
      A series of threats marked by ominous letters containing orange pips.
      Smaller cast but heavier on background knowledge, implied danger, and incomplete information — interesting for **uncertainty** and **weak evidence**.

    - **The Mysterious Affair at Styles**
      A full-length country house poisoning with multiple suspects, wills, timelines, and red herrings.
      Richest structure, perfect if you want a **denser graph** with layered motives and evolving hypotheses.

    /// admonition | Excercise 1.

    Pick **one** story to use as your case file and load it like this:
    ///
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    from neuro_noir.datasets import (
        the_adventure_of_retired_colorman,
        the_adventure_of_the_three_students,
        the_five_orange_pips,
        the_mysterious_affair_at_styles,
    )

    doc = the_adventure_of_retired_colorman()  # or any of the others
    [first, *rest] = doc.content.split('\n\n')
    exerpt = '\n\n'.join(rest[:10])[:560]
    mo.md(f"""
    ### {doc.title}

    **id:** _"{doc.id}"_

    /// details | {first}
    {exerpt}
    ///
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## From Story to Episodes (Chunking / Segmentation)

    Before we can extract entities and build a reasoning graph, we need to break the full story into **smaller, coherent pieces**. This step is often called **chunking** (yes, that’s a real and widely-used term), but you can also think of it as **segmenting** the story into **episodes**.

    /// admonition | Excercise 2.

    Write a function that takes a `Document` and returns a `list` of `Chunk` objects (e.g. `List[Chunk]`), where each chunk contains a meaningful slice of `doc.content`.

    ```python
    class Chunk(BaseModel):
        id: str          # e.g. f"{doc.id}-chunk-{i}"
        order: int       # position in the story
        title: str       # short label (optional)
        text: str        # the actual content of this chunk
    ```
    ///

    /// details | Why chunking matters
        type: info

    Good chunking has a big impact on your reasoning quality:

    - **Too large**
      The model sees everything at once, mixes suspects, scenes, and timelines; extraction becomes noisy and unfocused.
    - **Too small**
      A single chunk lacks context; you lose who is speaking, why something matters, or how events connect.
    - **Just right**
      Each chunk captures a **coherent scene, conversation, or step in the investigation**, so entities, claims, alibis, and contradictions are traceable to specific text.

    ///

    /// details | Possible chunking strategies
        type: info

    1. **Fixed-size segments (by length)**
       - Split the story into chunks of roughly *N* characters or words (e.g. 800–1500 chars).
       - ✅ Very simple.
       - ❌ May cut through scenes or conversations at awkward points.

    2. **Paragraph-based segments**
       - Split on blank lines, then accumulate paragraphs until you hit a target size.
       - ✅ Aligns with natural breaks.
       - ⚠️ Dialogue-heavy text (many short lines) may need merging to keep context intact.

    3. **Scene-oriented segments (semantic grouping)**
       - Aim for one location / event / conversational thread per chunk.
       - Implement via:
         - paragraph grouping + heuristics (new time/place/topic → new chunk), or
         - a small LLM helper to suggest boundaries.
       - ✅ Best for reasoning and traceability.
       - ❌ Requires a bit more effort.

    A good starting point for this workshop is: **paragraph-based with a soft size limit**, and iterate toward **scene-oriented** if time allows.
    ///
    """)
    return


@app.cell
def _(app):
    from neuro_noir.models.document import Document
    from neuro_noir.models.chunk import Chunk

    def do_the_chunking(doc: Document) -> list[Chunk]:
        ...


    app.register_chunker(do_the_chunking)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Chunking Hints

    /// details | Hint 1
        type: info

    ///

    /// details | Hint 2
        type: info

    ///

    /// details | Hint 3
        type: info

    ///

    /// details | Solution
        type: warn

    ```python
    from neuro_noir.models.document import Document
    from neuro_noir.models.chunk import Chunk

    MAX_CHUNK_SIZE = 800

    def do_the_chunking(doc: Document) -> list[Chunk]:
        chunks = []
        chunk_content = "\"
        paragraphs = doc.content.split('\n\n')

        for paragraph in paragraphs:
            if len(paragraph) + len(chunk_content) > MAX_CHUNK_SIZE:
                chunks.append(Chunk(
                    index=len(chunks),
                    document=doc.id,
                    title=f"Chunk {len(chunks) + 1}",
                    content=chunk_content,
                ))
                chunk_content = paragraph
            else:
                chunk_content += "\n\n" + paragraph

        return chunks


    app.register_chunker(do_the_chunking)
    ```

    ///
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## From Text to Knowledge Graph: Neo4j, Graphiti & Your Schema

    Now that you’ve split the story into episodes, the next step is to turn those episodes into a **knowledge graph** we can reason over.

    At its core, a knowledge graph is built from simple building blocks:

    - **Entities**: the “things” in your world
      e.g. people, locations, events, objects, organizations.
    - **Relations** (edges): how those things are connected
      e.g. *was at*, *knows*, *owns*, *sent*, *inherited from*.
    - Together, these form **triples** of the form:
      **subject – predicate – object**
      e.g. `Person B — was at — Café X`,
      `Person A — has motive — Victim`,
      `Letter — was sent to — Person C`.

    We will store these entities and relations in **Neo4j**, a native graph database, and use **Graphiti** as the layer that:

    - takes episode text,
    - uses an LLM to extract entities and relations,
    - writes them into Neo4j with embeddings and metadata,
    - lets us search and reason over this structured representation.

    To make this graph meaningful for our mystery domain, we won’t stick to only generic “Entity” and “RELATES_TO” nodes. Instead, we’ll define **custom types**, such as:

    - `Person`, `Location`, `Event`, `Evidence`, `Alibi`
    - edges like `WAS_AT`, `WITNESSED_BY`, `HAS_MOTIVE`, `USES_MEANS`, `CONTRADICTS`

    In the next steps, you’ll:

    1. Design a small domain schema that fits your chosen story.
    2. Implement these as **custom entity and edge types** in Graphiti.
    3. Use them to turn narrative episodes into a navigable, queryable case graph.
    """)
    return


@app.cell
def _():
    import marimo as mo
    from neuro_noir.core.config import Settings
    from neuro_noir.core.connections import verify_neo4j, verify_dspy, connect_neo4j

    cfg = Settings()
    return cfg, mo, verify_dspy, verify_neo4j


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
