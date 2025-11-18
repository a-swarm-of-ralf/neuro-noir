import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Workshop Neuro-Noir

    Step into a world where classic whodunits meet modern AI: in this workshop, you’ll use neurosymbolic techniques to teach machines to reason about suspects, motives, alibis, and contradictions—step by step, and in the open.

    ![spy](public/spy.jpg)

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
    ## Contents

    1. **Test Settings**: Test your connections to the database and languge model.
    1. **Select a Case**: Select one of the four cases to use in your workshop.
    2. **Create Schema**: Create a schema for the knowledge graph.
    3. **Chunk the Text**: Split the story into segments to process.
    4. **Create Knowledge Graph**: Run your segements with the schema to create the knowledge graph.
    5. **Enhance Knowledge Graph**: Add some logic derivations to the knoweldge graph.
    6. **Query the Knowledge Graph**: Query the Knowledge Graph
    7. **Create Reasoning Agent**: Create an Agent that can use the Knowledge Graph to reason about the case.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    run_test_neo4j = mo.ui.run_button(label="Test Database", kind="info", full_width=True)
    run_test_dspy = mo.ui.run_button(label="Test Language Model", kind="info", full_width=True)
    run_delete_neo4j = mo.ui.run_button(label="💀💀💀Delete Database 💀💀💀", kind="danger", full_width=True)

    mo.md(f"""
    ## 1. Test Settings

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
def _(app, mo, run_test_neo4j, verify_neo4j):
    if run_test_neo4j.value:
        try:
            verify_neo4j(app.cfg)
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
def _(app, mo, run_test_dspy, verify_dspy):
    if run_test_dspy.value:
        try:
            verify_dspy(app.cfg)
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
def _(app, mo, run_delete_neo4j, verify_dspy):
    if run_delete_neo4j.value:
        try:
            verify_dspy(app.cfg)
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
    ## 2. Select a Case

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


@app.cell(hide_code=True)
def _(list_datasets, mo):
    cases_dropdown = mo.ui.dropdown(options=list_datasets(), value="the-adventure-of-the-retired-colourman", full_width=True)
    run_load_case = mo.ui.run_button(label="Load!", kind="info", full_width=True)

    mo.md(f"""
    #### Select Your Case

    Select your case then press _'Load!'_.

    {cases_dropdown}
    {run_load_case}
    """)
    return cases_dropdown, run_load_case


@app.cell(hide_code=True)
def _(app, cases_dropdown, run_load_case):
    doc = app.doc
    if run_load_case.value:
        doc = app.load_document(cases_dropdown.value)
    return (doc,)


@app.cell(hide_code=True)
def _(doc, mo):
    mo.md(f"""
    #### Case: {doc.title}

    **id:** _"{doc.id}"_

    /// details | {doc.paragraphs[0]}

    {doc.paragraphs[1]}
    ///

    **Statistics:** 
    - {len(doc.content)} characters
    - {len(doc.chunks)} chunks
    - {len(doc.paragraphs)} paragraphs
    - {len(doc.annotations)} annotated paragraphs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(f"""
    ## 3. Create Schema

    Define a concise Graphiti schema for your mystery: entity and relationship types, their properties, and constraints, so extracted facts land in a consistent Neo4j structure. Graphiti then validates, embeds, and stores nodes and edges.

    A knowledge graph uses:
    - Entities — things (people, locations, events, objects, organizations)
    - Relations — how things connect (was at, knows, owns, sent, inherited from)
    - Triples — subject–predicate–object, e.g.:
      `Person B — was at — Café X`, `Person A — has motive — Victim`, `Letter — was sent to — Person C`

    We store the graph in Neo4j and use Graphiti to:
    - parse episode text with an LLM,
    - extract entities and relations,
    - write them with embeddings and metadata,
    - enable search and reasoning.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### 3.1 Create Entities

    Entities are the “things” in your mystery: people, places, objects, events, organizations, and evidence items. In Graphiti, you define these entities as structured data models. Once defined, Graphiti uses an LLM to extract instances of these models from text and writes them into Neo4j as nodes, with properties and embeddings.

    /// details | Why Pydantic BaseModel?
        type: info

    - Structure and validation: Pydantic’s BaseModel lets you declare the shape and types of your entities (strings, ints, bools, enums, etc.) and validates values at runtime.
    - Clear contracts for extraction: The model’s fields and types tell the LLM exactly what to look for and how to serialize it.
    - Documentation-first prompts: Class docstrings and Field descriptions become the guidance text that Graphiti includes in LLM prompts, dramatically improving extraction quality and consistency.
    ///


    /// details | How your model text guides the LLM?
        type: info

    - Class docstring: Sets the overall purpose and scope of the entity. Use it to clarify what belongs here and what does not.
    - Field descriptions: Tell the LLM what each attribute means, how to phrase it, when to use None, and any constraints (e.g., “choose from {suspect, victim, witness}”).
    - Names and examples: Use precise names; where relevant, provide short examples in descriptions.
    ///

    /// details | Example: A well-documented Person entity

    ```python
    from typing import Optional, Literal
    from pydantic import BaseModel, Field

    class Person(BaseModel):
        "\""A person involved in the detective case (suspect, victim, witness, investigator, or related party).

        Include named individuals explicitly referenced in the text. Do not create generic people
        (e.g., "the crowd") unless they act as a specific participant with a role in the case.
        "\""

        full_name: Optional[str] = Field(
            None,
            description="The person's full name as written in the text (e.g., 'Mr. Josiah Amberley')."
        )
        alias: Optional[str] = Field(
            None,
            description="Alternative name, nickname, or title (e.g., 'the retired colourman', 'Inspector')."
        )
        role_in_case: Optional[Literal["suspect", "victim", "witness", "investigator", "other"]] = Field(
            None,
            description="Primary role in the investigation. Choose one label that best fits the text evidence."
        )
        is_suspect: Optional[bool] = Field(
            None,
            description="True if the narrative treats this person as a suspect at any point; otherwise False."
        )
    ```
    ///

    /// details | Example: Location entity

    ```python
    class Location(BaseModel):
        "\""A place referenced in the case (home, office, shop, train station, room, or outdoor site).

        Prefer concrete, named locations. If a sub-area is important (e.g., 'the strong-room'), capture it.
        "\""

        name: str = Field(
            ...,
            description="Canonical name of the location as stated in the text (e.g., 'Camden House', 'Strong-room')."
        )
        address: Optional[str] = Field(
            None,
            description="Street address or descriptive locator if present (e.g., 'Little Ryder Street, Westminster')."
        )
        kind: Optional[Literal["residence", "business", "room", "public", "transport", "other"]] = Field(
            None,
            description="General category of the place to aid reasoning about access and movement."
        )
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    /// details | Best practices for defining entities
        type: info

    - Be specific and consistent: Use stable names and clear categories so the LLM doesn’t invent variants.
    - Prefer Optional fields over guessing: If the text doesn’t provide a value, allow None rather than hallucination.
    - Constrain with Literals where helpful: Small controlled vocabularies improve precision.
    - Write actionable descriptions: Tell the LLM exactly what to extract, when to skip, and how to format.
    - Include evidence later: We will link extracted entities to their source text (chunks) so you can trace every fact.

    ///


    /// admonition | Excercise 2.1.

    Create Entities for your project.

    - Start with a small set of core entities (Person, Location, Object/Event).
    - Ensure each class has a concise docstring and each Field has a descriptive explanation.
    - Reuse or adapt the Person model defined above in this notebook as your canonical Person entity.
    ///
    """)
    return


@app.cell
def _(BaseModel, Field, Optional):
    class Person(BaseModel):
        """A person involved in a detective case (suspect, victim, witness, investigator, or other role)."""

        full_name: Optional[str] = Field(None, description="Full name of the person as mentioned in the materials.",)
    return (Person,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    /// details | Best practices for defining edges (relationships) in Graphiti
        type: info

    - **Edge Types:** Use PascalCase for custom types (e.g., Employment, Partnership)
    - **Attributes:** Use snake_case (e.g., start_date, employee_count)
    - **Descriptions:** Be specific and actionable for the LLM

    ///


    /// admonition | Excercise 2.2.

    Create Edges for your case in Graphiti.

    - Identify 3–5 core relationships that matter for your case (e.g., `Person` -> `WorksAt` -> `Organization`, `Document` -> `Mentions` -> `Entity`, `Event` -> `OccursAt` -> `Location`).

    ///
    """)
    return


@app.cell
def _(BaseModel, Field, Literal, Optional):
    class CommunicatedWith(BaseModel):
        """Relationship indicating that one Person communicated with another Person."""

        communication_type: Optional[
            Literal["talked_to", "wrote_to", "shouted_at", "agreed_with", "disagreed_with"]
        ] = Field(
            None,
            description=(
                "Subtype of communication linking the two Persons. "
                "Examples include direct conversation, shouting, or explicit agreement. "
                "If the subtype is unknown, leave this as None."
            ),
        )
        justification: Optional[str] = Field(
            None,
            description="Brief natural-language explanation of how the source text indicates this communication between the two Persons (e.g., a quote or summary).",
        )
    return (CommunicatedWith,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    With the entities and edges defined, the next step is to build the relationship mapping that connects them.

    /// admonition | Exercise 2.3.

    Create the edge mapping for your Graphiti model.

    - For each pair of entities, list the edge types that apply between them.
    - If edges are directional, consider both directions (A → B and B → A).
    - If no edges apply for a pair, use an empty list.

    ///
    """)
    return


@app.cell
def _(CommunicatedWith, Person):
    entity_types = {
        "Person": Person
    }

    edge_types = {
        "CommunicatedWith": CommunicatedWith
    }

    edge_type_map = {
        ("Person", "Person"): ["CommunicatedWith"]
    }
    return edge_type_map, edge_types, entity_types


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Chunking

    Before we can extract entities and build a reasoning graph, we need to break the full story into **smaller, coherent pieces**. This step is often called **chunking** (yes, that’s a real and widely-used term), but you can also think of it as **segmenting** the story into **episodes**.

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

    /// admonition | Excercise 3.

    Write a function that takes a `Document` and returns a `list[str]` of _chunks_, where each chunk contains a meaningful slice of `doc.content`.

    ///
    """)
    return


@app.cell
def _(Document):
    def do_the_chunking(doc: Document) -> list[str]:
        # Your chunk logic here
        ...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 5. Generate Knowledge Graph

    /// admonition | Excercise 4.

    For each chunk ingest it into the database by calling the `neuro_noir.core.database.add_episode` function.

    ///
    """)
    return


@app.cell
async def _(
    add_episode,
    app,
    connect_graphiti,
    doc,
    edge_type_map,
    edge_types,
    entity_types,
    mo,
):
    chunks = ...  # Do chunking here..
    graphiti = connect_graphiti(app.cfg)
    async def _():
        for idx, chunk in enumerate(mo.status.progress_bar(chunks)):
            result = await add_episode(graphiti, doc, chunk, idx, entity_types, edge_types, edge_type_map)

    await _()
    return chunks, graphiti


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 6. Enhance Knowledge Graph

    After generating your graph, open it in Neo4j Desktop and explore it interactively.
    Click through different nodes and relationships to understand what has been created—and, just as importantly, what is missing.

    During this inspection, you will likely notice that some expected entities or relationships are absent.
    Part of this can be improved by refining your Entity and Edge definitions and descriptions.
    However, some missing information is not directly stated in the source text. Graphiti focuses on extracting explicit facts and does not infer new ones.

    A reasoning model—such as GPT-5—can infer additional facts that are implied but not written.
    By integrating such reasoning into DSPy, we can generate new inferred knowledge and feed it back into Graphiti as additional episodes.

    /// admonition | Excercise 5.

    Create and run a DSPy model that derives additional facts and ingests them into the Knowledge Graph.

    **Goal:**
    - Use a reasoning LLM to infer missing facts from existing episodes.
    - Generate new structured records that match your graph schema.
    - Import these inferred facts back into Graphiti as new episode inputs.
    ///
    """)
    return


@app.cell
def _(dspy):
    # This is just an example custimize it to your needs.
    class InferConclusions(dspy.Signature):
        """
        Given a narrative episode text, infer additional facts and relationships
        that are implied but not explicitly stated.

        The output format must be structured as natural language paragraphs,
        suitable for ingestion into Graphiti as new episodes.
        """

        episode_text: str = dspy.InputField(desc="Original episode text from which to infer missing knowledge")
        conclusions: str = dspy.OutputField(
            desc=(
                "One or more natural language paragraphs describing inferred entities, "
                "relationships, or facts not explicitly stated in the episode text. "
                "Write as plain sentences that Graphiti can process as new input."
            )
        )
    inferer = dspy.ChainOfThought(InferConclusions)
    return (inferer,)


@app.cell
def _(chunks, inferer):
    # Let's try it with the first chunk
    inferer(episode_text=chunks[0])
    return


@app.cell
async def _(
    add_episode,
    chunks,
    doc,
    edge_type_map,
    edge_types,
    entity_types,
    graphiti,
    inferer,
    mo,
):
    async def _():
        for idx, chunk in enumerate(mo.status.progress_bar(chunks)):
            inferer_result = inferer(episode_text=chunk)
            await add_episode(graphiti, doc, inferer_result.conclusions, idx, entity_types, edge_types, edge_type_map)

    await _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 7. Query Knowledge Graph

    Once your Knowledge Graph has been populated with extracted and inferred facts, the next step is to retrieve useful information from it.

    Graphiti provides a **search-based API** rather than requiring you to write Cypher directly. The main entry point is the search method:

    - `await graphiti.search(query)`
    - `await graphiti.search(query, focal_node_uuid)`

    Under the hood, Graphiti combines **semantic similarity** and **BM25** keyword search, then reranks results using **Reciprocal Rank Fusion (RRF)**. This is called Hybrid Search and is designed to return the most relevant facts (edges) for a natural-language query.

    If you provide a focal_node_uuid of a specific entity, Graphiti additionally reranks results based on their graph distance to that node. This is called **Node Distance Reranking** and is particularly useful for _entity-centric_ questions (e.g. “What do we know about Elyra?”).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    /// admonition | Exercise 6.

    Create and run queries against your Knowledge Graph using Graphiti’s search API.

    Tasks:

    1. Basic hybrid search
        - Pick a natural-language question about your story or domain.
        - Call graphiti.search(query) and print the returned edge.fact strings.
        - Inspect whether these facts match your expectations.
    2. Entity-focused search
        - Choose a specific entity (e.g. a main character, organization, or location).
        - Obtain its node UUID (for example from a previous query or from your graph tooling).
        - Call graphiti.search(query, focal_node_uuid) with the same query.
        - Compare the ranking of results with the basic search: do you see more facts about that entity?
    ///

    ➡️ Make sure to take note of the exact output structure returned by `graphiti.search()`—you will need this format in the next exercise.
    """)
    return


@app.cell
def _(graphiti):
    graphiti.search("What do we know about Sherlock Holmes?")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 8. Create Agent

    Up to this point, you have:

    - Built and enriched a Knowledge Graph using Graphiti
    - Queried it directly using `graphiti.search(...)`

    Now it’s time to let a **DSPy agent** use the graph as part of its own reasoning.

    In this section, we will build a **`dspy.ReAct` agent** that:

    - Receives a **natural-language question**
    - Thinks step-by-step (ReAct prompting)
    - Calls `graphiti.search` as a **tool**, but *only when it decides that it needs the information*
    - Integrates retrieved facts into its reasoning
    - Produces a high-quality answer
    - Runs inside a simple **chat loop**

    This transforms your Knowledge Graph from a static resource into a **dynamic tool** that actively enhances model reasoning.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The agent becomes capable of:

    - Looking up missing context
    - Checking facts
    - Combining retrieved graph data with its own reasoning
    - Answering complex, multi-step questions grounded in your graph

    A typical setup involves:

    1. A **Signature** describing what the agent takes as input and returns as output
    2. A **tool function** wrapping `graphiti.search`
    3. A **ReAct agent** configured to use that tool
    4. A **chat loop** letting you interact with the agent turn by turn
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | Exercise 7.
    Create a **DSPy ReAct agent** that uses `graphiti.search` as a tool inside a chat loop.

    **Tasks:**

    1. **Define a Signature**
       - Create a signature (e.g. `AnswerWithGraph`) with:
         - `question: str` (input)
         - `answer: str` (output)
         - Optional: `chat_history: str` so the agent sees prior turns.

    2. **Wrap Graphiti search as a tool**
       - Implement a function like `graph_search_tool(query: str) -> str` that:
         - Calls `graphiti.search(query)`
         - Extracts `edge.fact` fields
         - Returns them as a readable text block
         - Includes a clear docstring (DSPy uses this to understand tool behavior)

    3. **Instantiate a `dspy.ReAct` agent**
       - Attach the tool to the agent via `tools=[...]`
       - Ensure the agent uses your signature

    4. **Build a simple chat loop**
       - Prompt the user for input
       - Pass the question (and history) to the agent
       - Print the answer
       - Append both user and agent messages to `history`

    **Goal:**
    By the end of this exercise, you will have a functioning **knowledge-augmented chat agent** that can decide on its own when to retrieve facts from your Knowledge Graph.

    Make sure to pay attention to the **output format of `graphiti.search`**, since you will be feeding it directly into your agent’s reasoning.

    ///
    """)
    return


@app.cell
def _(asyncio, dspy, graphiti):
    class ChatAgent(dspy.ChatSignature):
        """
        A multi-turn chat agent that can use tools and DSPy reasoning.
        """
        messages: dspy.Messages = dspy.InputField()
        answer: str = dspy.OutputField()

    def graph_search_tool(query: str) -> str:
        """
        Use graphiti.search (async) under the hood to retrieve relevant facts
        from the Knowledge Graph for the given natural-language query.
        Returns a concise textual summary of the most important facts.
        """
        async def _run() -> str:
            edges = await graphiti.search(query)
            return "\n".join(edge.fact for edge in edges)

        return asyncio.run(_run())

    agent = dspy.ReAct(
        ChatAgent,
        tools=[graph_search_tool],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 💬 Optional: Integrate Your Agent into a Marimo Chat Interface

    If you’re running this project inside **Marimo**, you get access to a powerful UI feature:
    **`marimo.ui.chat` — an interactive chat widget.**

    This widget lets you embed a live conversational interface directly in your notebook.
    Because the chat model function can run **async Python**, it can call `graphiti.search` naturally and integrate perfectly with your DSPy agent.

    /// admonition | **Optional Final Exercise — Integrate Your ReAct Agent into a Marimo Chat Widget**

    As a bonus challenge:

    **Hook your DSPy ReAct agent into a `marimo.ui.chat` widget** so you can talk to it naturally inside the notebook.
    ///

    ![tools](public/tools.jpg)
    """)
    return


@app.cell
def _(mo):
    def my_agent_model(messages, config):
        # Each message has a `content` attribute, as well as a `role`
        # attribute ("user", "system", "assistant");

        # agent logic here
        response = "My agent does nothing yet"

        return response


    chat = mo.ui.chat(my_agent_model)

    chat
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo

    from typing import Optional, Literal

    from pydantic import BaseModel, Field
    import dspy
    import asyncio

    from neuro_noir.core.config import Settings
    from neuro_noir.core.connections import (
        verify_neo4j,
        verify_dspy,
        connect_neo4j,
        connect_graphiti,
    )
    from neuro_noir.datasets import list_datasets, load_dataset
    from neuro_noir.core.app import Application
    from neuro_noir.models.document import Document
    from neuro_noir.core.database import add_episode

    app = Application()
    return (
        BaseModel,
        Document,
        Field,
        Literal,
        Optional,
        add_episode,
        app,
        asyncio,
        connect_graphiti,
        dspy,
        list_datasets,
        mo,
        verify_dspy,
        verify_neo4j,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
