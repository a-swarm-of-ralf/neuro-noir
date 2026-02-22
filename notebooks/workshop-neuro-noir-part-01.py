import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    # Workshop Neuro-Noir

    Step into a world where classic whodunits meet modern AI: in this workshop, you’ll use neurosymbolic techniques to teach machines to reason about suspects, motives, alibis, and contradictions—step by step, and in the open.

    _![image of spy](public/spy.jpg)_

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
    mo.md(rf"""
    ## Contents

    1. **Test Settings**: Test your connections to the database and languge model.
    1. **Select a Case**: Select one of the four cases to use in your workshop.
    2. **Create Schema**: Create a schema for the knowledge graph.
    3. **Chunk the Text**: Split the story into segments to process.
    4. **Create Knowledge Graph**: Run your segements with the schema to create the knowledge graph.
    5. **Enhance Knowledge Graph**: Add some logic derivations to the knoweldge graph.
    6. **Query the Knowledge Graph**: Query the Knowledge Graph
    7. **Create Reasoning Agent**: Create an Agent that can use the Knowledge Graph to reason about the case.

    /// attention | Run the Notebook!

    Start with running the entire notebook with the {mo.icon('lucide:circle-play')} button in the bottom right. This enables all the ui elements.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Settings

    The notebook should already be set up correctly by the workshop coordinators. After running the notebook, buttons will appear in the sidebar on the left. Click each one to verify that all settings are working properly.

    These buttons perform the following actions:

    - **Test Database**
      Tests the connection to the Neo4j graph database.

    - **Test Completion**
      Tests the connection and configuration of the DSPy large language model (LLM) completion service.

    - **Test Embedding**
      Tests the connection to the embedding model used to create vector embeddings for information retrieval.

    - **Delete Database**
      Permanently deletes all data in the database. This action does **not** show a warning or confirmation prompt. Use with extreme caution.

    Once all tests complete successfully, enter your name in the **User** section of the same sidebar.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Case

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

    /// attention | Story Size

    _The Mysterious Affair at Styles_ is a full-sized novel. This means ingesting it can take quite a lot of time, upto multiple hours! So it is not recommened if you quickly want results.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(cases_dropdown, mo, run_load_case):
    mo.md(rf"""
    ### Select Your Case

    /// admonition | Excercise 1.

    Pick **one** story to use as your case file and load it in the form below.
    ///

    Select your case then press _'Load!'_.

    {cases_dropdown}
    {run_load_case}
    """)
    return


@app.cell(hide_code=True)
def _(doc, mo):
    mo.md(rf"""
    ### Case: {doc.title}

    **id:** _"{doc.id}"_

    /// details | {doc.paragraphs[0]}

    {doc.chunks_per_paragraph(chunk_size=400)[0]}
    ///

    **Statistics:** 
    - {len(doc.content)} characters
    - {len(doc.paragraphs)} paragraphs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Chunking

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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### Chunk Your Case

    /// admonition | Excercise 2.

    Write a function called `do_the_chunking` that takes a `text` string and returns a `list[str]` of _chunks_, where each chunk contains a meaningful slice of the `text`.

    ///

    The cell below has a scaffold for the function.
    """)
    return


@app.function
def do_the_chunking(text: str) -> list[str]:
    chunks = []
    # Your chunk logic here
    ...
    # My Chunk Logic - TODO: Remove before Workshop
    chunk_size: int = 800
    min_chunk_size: int = 100
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    chunk = ""
    for paragraph in paragraphs:
        if len(chunk) + len(paragraph) <= chunk_size:
            # If adding the paragraph doesn't exceed the chunk size, add it to the 
            # active chunk
            chunk += "\n\n" + paragraph if chunk else paragraph
        elif len(chunk) < min_chunk_size:
            # If active is too small, we don't want to break it up
            chunk += "\n\n" + paragraph if chunk else paragraph
        else:
            # If adding the paragraph exceeds the chunk size, save the active chunk and 
            # start a new one
            if chunk:
                # Only save the active chunk if it's not empty. This could happen if the 
                # first paragraph is larger than the chunk size, in which case we want to 
                # save it as its own chunk
                chunks.append(chunk.strip())
            chunk = paragraph
    # The last chunk might not have been added if we reached the end of the paragraphs without 
    # exceeding the chunk size. Also, the last chunk can be smaller than the min_chunk_size, 
    # but that's okay since it's the last chunk
    if chunk:
        chunks.append(chunk.strip())
    return chunks


@app.cell(hide_code=True)
def _(mo, run_chunk_case):
    mo.md(rf"""
    ### Start Chunking

    **_Run_** the cell above and _then_ press the 'Chunk!'button below.

    {run_chunk_case}

    /// details | {mo.icon('fluent-color:warning-16')} Trouble with chunking? Check this! **{mo.icon('fluent-color:warning-16')}_Spoilers..._** {mo.icon('fluent-color:warning-16')}
        type: warn

    Here is my solution:

    1. First we create paragraphs by splitting the text on double newline (\\n\\n).
    2. Then we go through each paragraph gather them together into a chunk until we have a chunk of acceptable size.
    3. When we have a chunk of acceptable size we store it and start a new chunk.

    Or in code:

    ```python
    def do_the_chunking(text: str) -> list[str]:
        chunks = []
        chunk_size: int = 800
        min_chunk_size: int = 100
        paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
        chunk = "\"
        for paragraph in paragraphs:
            if len(chunk) + len(paragraph) <= chunk_size:
                # If adding the paragraph doesn't exceed the chunk size, add it to the 
                # active chunk
                chunk += "\n\n" + paragraph if chunk else paragraph
            elif len(chunk) < min_chunk_size:
                # If active is too small, we don't want to break it up
                chunk += "\n\n" + paragraph if chunk else paragraph
            else:
                # If adding the paragraph exceeds the chunk size, save the active chunk and 
                # start a new one
                if chunk:
                    # Only save the active chunk if it's not empty. This could happen if the 
                    # first paragraph is larger than the chunk size, in which case we want to 
                    # save it as its own chunk
                    chunks.append(chunk.strip())
                chunk = paragraph
        # The last chunk might not have been added if we reached the end of the paragraphs without 
        # exceeding the chunk size. Also, the last chunk can be smaller than the min_chunk_size, 
        # but that's okay since it's the last chunk
        if chunk:
            chunks.append(chunk.strip())
        return chunks
    ```
    """)
    return


@app.cell(hide_code=True)
def _(chunk_carousel, chunks, mo):
    mo.md(rf"""
    ### View Chunks - {len(chunks)}

    {chunk_carousel}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### Checkout the Graph

    If all went well the chunks should have been inserted into the graph database. Check it out. It should look something like this:

    ![Image of Graph with Chunk Nodes](public/graph-chunks.jpg)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### Querying Chunks

    Now that we have inserted our chunks we can query them. This works through embeddings.

    /// details | Embeddings
        type: info

    If you examine the chunk nodes in **Neo4j** you’ll notice an attribute called _embedding_. An **embedding** is a numerical representation of the meaning of a piece of text, created by a machine learning model. Instead of storing words as plain strings, the model converts the content of a chunk into a long list of numbers (in your case, 1536 values) that captures its semantic context. Texts with similar meanings will have embeddings that are mathematically close to each other, even if they use different wording. For example, “The cat sits on the mat” and “A feline is resting on the rug” will produce embeddings that are very similar, despite sharing few exact words.

    These embeddings allow you to perform **semantic search** and clustering instead of relying only on keyword matching. When you embed a user query, you can compare it to the stored chunk embeddings and find the most relevant pieces of text using similarity measures such as **cosine similarity**. This makes it possible to build features like “search by meaning,” recommendation systems, and retrieval-augmented generation (RAG) pipelines. In practice, this means your application can retrieve the most relevant chunks for a question, even when the question does not use the same vocabulary as the original document, leading to more robust and intelligent behavior.

    ///

    /// admonition | Excercise 3.

    Let's try it. Use `app.search_chunks("[my-query]")` to search our chunks.

    ///
    """)
    return


@app.cell
def _():
    # app.search_chunks("Blackheath Station")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Generating the Knowledge Graph

    Now we have the our schema and the chunks we can extract the knowledge graph from this information.

    /// details | Triples
        type: info

    A knowledge graph consists of **[_subject_ → _verb_ → _object_]** statements. These are often called **triples**, and they provide a simple, structured way to represent facts. Each triple captures one basic idea: something (**the subject**) is related in some way (**the verb**) to something else (**the object**). For example:

    - **Alice → works at → CompanyX**
    - **Paris → is capital of → France**

    By breaking information down into these small, consistent pieces, complex text can be transformed into data that computers can reliably store, query, and connect. Instead of parsing entire paragraphs every time, systems can operate on these atomic building blocks of meaning.

    On their own, triples are admittedly **limited**. They do not easily capture nuance, uncertainty, emotions, or long narrative context. However, their simplicity is precisely what makes them powerful. Because every fact follows the same structure, triples can be **linked together into networks**, queried efficiently, and combined across different data sources. While a single triple may seem trivial, thousands or millions of them form a **graph of interconnected knowledge** that enables structured search, relationship discovery, and even reasoning. In short, triples trade expressive richness for **scalability, consistency, and computability**—a trade-off that makes them extremely valuable in software systems.

    ///

    We use [DSPy](https://dspy.ai/) to extract triples from our chunks. A slider is provided to select the number of chunks to givbe to the extraction.

    /// details | DSPy
        type: info

    We use **[DSPy](https://dspy.ai/)**, a **declarative framework for AI software**, for the extraction and optimization of structured information from text. Instead of manually crafting and fine-tuning prompts, DSPy allows developers to describe *what* they want the model to produce using clear input–output specifications, examples, and constraints. These specifications are then used by DSPy to automatically generate, evaluate, and refine prompts. This shifts prompt engineering from an ad-hoc, trial-and-error process into a more systematic and reproducible development workflow.

    By treating prompts as trainable programs rather than static strings, DSPy enables continuous improvement of extraction quality through automated optimization techniques. It can test multiple prompt variants, measure their performance against examples, and converge on better-performing configurations over time. For this project, this means that tasks such as extracting entities, relationships, and statements can be made more reliable, consistent, and maintainable. Instead of relying on fragile, hand-written prompts, we use DSPy to build adaptive pipelines that improve as more data and feedback become available.

    ///

    /// attention | Chunk Limit
    Extracting can take quite some time, so keep the number of chunks small and examine the result trying the full run.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(extraction_chunk_limit_slider, mo, run_extract_case):
    mo.md(rf"""
    ### Extract Triples

    /// admonition | Exercise 4.

    Run the extraction and examine the results.
    ///

    {extraction_chunk_limit_slider}
    {run_extract_case}
    """)
    return


@app.cell
def _(app, extraction_chunk_limit_slider, mo, run_extract_case):
    triples = []
    _params = {
        'title': f"Extracting Triples",
        'subtitle': f"processing {extraction_chunk_limit_slider.value} chunks..."
    }

    if run_extract_case.value:
        app.start_extraction()
        for _chunk in mo.status.progress_bar(app.chunks[:extraction_chunk_limit_slider.value], **_params):
            app.do_extraction(_chunk)
        triples = app.end_extraction()
    return (triples,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examining the Extractor

    The extractor is a DSPy module that contains an language model prompt. Writing the prompt

    /// details | Extractor
        type: info

    ```python
    class ExtractStatements(Signature):
        "\"\"
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
            - Add other modalities as needed, but be careful to not add too many modalities that are not relevant or useful for understanding the statement.
            - Note that a statement can have multiple modalities. For example, if the statement is 'The cat might not be on the mat', the modalities would be 'possibility' and 'negation'.
        5. Add an explanation about why the subject, predicate, and object were chooses and why it has that modality.

        Return a JSON array where each item is one statement with metadata.
        "\"\"
        text: str = InputField(desc="The text to extract statements from.")

        statements: list = OutputField(
            desc="JSON array of {subject, predicate, object, modality, sentence, explanation}",
            json_schema=STATEMENTS_SCHEMA
        )
    ```

    ///
    """)
    return


@app.cell
def _(mo, triples):
    mo.ui.table(
        data=[({ 
            "subject": trip.subject, 
            "predicate": trip.predicate, 
            "object": trip.object_,
            "modality": ", ".join(trip.modality) if trip.modality else "-",
            "sentence": trip.sentence,
            "explanation": trip.explanation,
            }) for trip in triples ],
        pagination=True,
        label="Triples",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Entities

    As you can see in the triple table not all subjects and objects we extracted are very useful. When extracting subject–verb–object statements from natural language, many of the resulting subjects and objects are initially **unhelpful or ambiguous**, such as “I,” “you,” “he,” “she,” or “it.” These words carry little meaning on their own without context. Our next task is therefore to **resolve these references** into concrete, identifiable concepts by performing entity resolution, coreference resolution, and disambiguation.

    /// details | Entities
        type: info

    In the context of triples and knowledge graphs, an **entity** is not a software object or a database record, but a real-world concept that can be uniquely identified and referred to across many statements. An entity represents something that “exists” in the domain of discourse: a person, organization, place, object, event, or abstract concept. For example, instead of treating “he,” “Watson,” and “the doctor” as separate subjects, they may all refer to the same underlying entity: *Dr. John Watson*. In RDF- and triple-based systems, entities act as stable anchors that connect many individual statements into a coherent network of knowledge.

    ///

    /// details | Coreference Resolution & Disambiguation
        type: info

    Two key processes help achieve this: **coreference resolution** and **disambiguation**. Coreference resolution identifies when different words or phrases in a text refer to the same entity, such as linking “the big cat,” “the cat,” and “it” to a single concept. Disambiguation, on the other hand, determines which specific entity is meant when a name or phrase could refer to multiple things, such as deciding whether “Paris” refers to the city in France or a person’s name. Together, these techniques transform vague or overloaded language into precise, reusable entities, making the resulting knowledge graph more accurate, connected, and useful for downstream reasoning and search.

    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// details | Why Pydantic BaseModel?
        type: info

    - Structure and validation: Pydantic’s BaseModel lets you declare the shape and types of your entities (strings, ints, bools, enums, etc.) and validates values at runtime.
    - Clear contracts for extraction: The model’s fields and types tell the LLM exactly what to look for and how to serialize it.
    - Documentation-first prompts: Class docstrings and Field descriptions become the guidance text that are included in LLM prompts, dramatically improving extraction quality and consistency.
    ///


    /// details | How your model text guides the LLM?
        type: info

    - Class docstring: Sets the overall purpose and scope of the entity. Use it to clarify what belongs here and what does not.
    - Field descriptions: Tell the LLM what each attribute means, how to phrase it, when to use None, and any constraints (e.g., “choose from \{suspect, victim, witness\}”).
    - Names and examples: Use precise names; where relevant, provide short examples in descriptions.
    ///

    /// details | Example: A well-documented Person entity

    ```python
    from typing import Optional, Literal
    from pydantic import BaseModel, Field

    class Person(BaseModel):
        "\"\"A person involved in the detective case (suspect, victim, witness, investigator, or related party).

        Include named individuals explicitly referenced in the text. Do not create generic people
        (e.g., "the crowd") unless they act as a specific participant with a role in the case.
        "\"\"

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
        "\"\"A place referenced in the case (home, office, shop, train station, room, or outdoor site).

        Prefer concrete, named locations. If a sub-area is important (e.g., 'the strong-room'), capture it.
        "\"\"
        # name is reserved
        location_name: str = Field(
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
    mo.md(r"""
    /// details | Best practices for defining entities
        type: info

    - Be specific and consistent: Use stable names and clear categories so the LLM doesn’t invent variants.
    - Prefer Optional fields over guessing: If the text doesn’t provide a value, allow None rather than hallucination.
    - Constrain with Literals where helpful: Small controlled vocabularies improve precision.
    - Write actionable descriptions: Tell the LLM exactly what to extract, when to skip, and how to format.
    - Include evidence later: We will link extracted entities to their source text (chunks) so you can trace every fact.

    ///

    /// attention | Protected Attribute Names

    Entity type attributes cannot use protected names that are already used by the core EntityNode class:

    - `id`
    - `name`
    - `aliases`
    - `type`
    - `category`
    - `description`
    - `explanation`
    - `attributes`

    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### Create Your Entities

    /// admonition | Excercise 5.

    Create Entities for your project.

    - Start with a small set of core entities (Person, Location, Object/Event).
    - Ensure each class has a concise docstring and each Field has a descriptive explanation.
    - Reuse or adapt the Person model defined above in this notebook as your canonical Person entity.
    ///
    """)
    return


@app.cell
def _(BaseModel, Field, Optional, app):
    class Person(BaseModel):
        """
        A person involved in a detective case (suspect, victim, witness, investigator, or other role).
        """
        full_name: Optional[str] = Field(default="", 
            description="Full name of the person as mentioned in the materials.",)

    class Organization(BaseModel):
        """
        A company
        """
        activities: str = Field(default="", 
            description="What does the organization do.",)

    class Location(BaseModel):
        """
        A location mentioned. Examples 'Home', 'Pemberly Station'
        """
        presence: str = Field(default="", description="Who is there.",)

    class Item(BaseModel):
        """
        An item that has some relevance, 'a letter', 'weapon', 'violin'
        """
        usage: str = Field(default="", description="How is the item used",)

    class Mood(BaseModel):
        """
        A mood somebody is in. 'Anger', 'Sadness', 'Happy', 
        """
        is_good: str = Field(default="", description="Is it a good or bad mood?",)

    app.clear_entities_and_relationships()
    app.register_entities([Person, Organization, Location, Item, Mood])
    return


@app.cell(hide_code=True)
def _(extraction_chunk_limit_slider, mo, run_resolve_case):
    mo.md(rf"""
    ### Resolve Entities

    /// admonition | Exercise 6.

    Define Entities and run the resolver.
    ///

    {extraction_chunk_limit_slider}
    {run_resolve_case}
    """)
    return


@app.cell
def _(app, extraction_chunk_limit_slider, mo, run_resolve_case):
    entities = []
    _params = {
        'title': f"Resolving Entities",
        'subtitle': f"processing {extraction_chunk_limit_slider.value} chunks..."
    }

    if run_resolve_case.value:
        app.start_resolution()
        for _chunk in mo.status.progress_bar(app.chunks[:extraction_chunk_limit_slider.value], **_params):
            app.do_resolution(_chunk)
        entities = app.end_resolution()
    return (entities,)


@app.cell
def _(entities, mo):
    mo.ui.table(
        data=[({ 
            "name": ent.name,
            "aliases": ", ".join(ent.aliases) if ent.aliases else "-",
            "type": ent.type_,
            "category": ent.category,
            "aliases": ", ".join(ent.aliases) if ent.aliases else "-",
            "description": ent.description,
            "explanation": ent.explanation,
            }) for ent in entities ],
        pagination=True,
        label="Entities",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Examine the Graph

    Now we have statements and entities in our graph it starts to look more like network and less like a tree.

    ![Graph with Statements and Entities](public/graph-entities.jpg)

    But we are not there yet. We still have entities that are essentially the same. We have multiple 'Holmes'and 'Watson' entities. To solve this we need _coreference resolution_, where we merge entities that are the same.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # ⛔ Stop Here

    You have now reached the end of the interactive part of this workshop.

    All cells below this point contain internal setup and helper code that is already configured for you. You do **not** need to read, modify, or run anything further to complete the exercises.

    Feel free to explore the code if you are curious, but for the purposes of this workshop, **you can safely stop here.** ✅

    Great work, and well done for making it this far!
    ---
    """)
    return


@app.cell
def _(app, list_datasets, mo):
    run_test_neo4j = mo.ui.run_button(label="Test Database", kind="info", full_width=True)
    run_test_dspy = mo.ui.run_button(label="Test Completion", kind="info", full_width=True)
    run_test_genai = mo.ui.run_button(label="Test Embedding", kind="info", full_width=True)
    run_delete_neo4j = mo.ui.run_button(label="💀 Delete Database 💀", kind="danger", full_width=True)

    user_name = mo.ui.text(value=app.user, placeholder="Student 123", full_width=True)

    cases_dropdown = mo.ui.dropdown(options=list_datasets(), value="the-adventure-of-the-retired-colourman", full_width=True)

    run_load_case = mo.ui.run_button(label="Load!", kind="info", full_width=True)
    run_chunk_case = mo.ui.run_button(label="Chunk!", kind="info", full_width=True)
    run_extract_case = mo.ui.run_button(label="Extract!", kind="info", full_width=True)
    run_resolve_case = mo.ui.run_button(label="Resolve Entities!", kind="info", full_width=True)
    return (
        cases_dropdown,
        run_chunk_case,
        run_delete_neo4j,
        run_extract_case,
        run_load_case,
        run_resolve_case,
        run_test_dspy,
        run_test_genai,
        run_test_neo4j,
        user_name,
    )


@app.cell
def _(app, cases_dropdown, run_load_case):
    doc = app.doc
    if run_load_case.value:
        doc = app.load_document(cases_dropdown.value)
    return (doc,)


@app.cell
def _(app, run_chunk_case, user_name):
    chunks = []
    if run_chunk_case.value:
        chunks = app.chunk_document(do_the_chunking, user=user_name.value)
    return (chunks,)


@app.cell
def _(chunks, mo):
    if len(chunks) > 1:
        chunk_carousel = mo.carousel([ mo.callout(mo.md(f"#### Chunk {chunk.index}\n\n{chunk.content}")) for idx,chunk in enumerate(chunks) ])
    else:
        chunk_carousel = mo.callout(mo.center(mo.md(f"no chunks found...")))
    return (chunk_carousel,)


@app.cell
def _(chunks, mo):
    extraction_chunk_limit_slider = mo.ui.slider(
        start=0,
        stop=len(chunks) or 1,
        value=1,
        show_value=True,
        label="Number Chunks to Extract",
        full_width=True
    )
    return (extraction_chunk_limit_slider,)


@app.cell
def _(app, mo, run_delete_neo4j, run_test_neo4j):
    db_ok = False
    db_line = "_not tested yet..._"
    db_details = "_not tested yet..._"

    if run_test_neo4j.value:
        db_ok, db_line, db_details = app.test_db()

    if run_delete_neo4j.value:
        db_ok, db_line, db_details = app.clear_db()

    mo.md(db_line) if db_ok else mo.md(db_details)
    return (db_line,)


@app.cell
def _(app, mo, run_test_dspy, run_test_genai):
    lm_ok = False
    lm_line = "_not tested yet..._"
    lm_details = "_not tested yet..._"

    if run_test_dspy.value:
        lm_ok, lm_line, lm_details = app.test_lm()

    if run_test_genai.value:
        lm_ok, lm_line, lm_details = app.test_embedding()

    mo.md(lm_line) if lm_ok else mo.md(lm_details)
    return (lm_line,)


@app.cell
def _(
    db_line,
    doc,
    lm_line,
    mo,
    run_delete_neo4j,
    run_test_dspy,
    run_test_genai,
    run_test_neo4j,
    user_name,
):
    mo.sidebar([
        mo.md("# Neuro Noir"),
        mo.md(f"## {mo.icon('fluent-color:edit-20')} Excercises"),
        mo.nav_menu({
            "#select-your-case": f"1. Select Your Case",
            "#chunk-your-case": f"2. Chunk Your Case",
            "#querying-chunks": f"3. Querying Chunks",
            "#extract-triples": f"4. Extract Triples",
            "#create-your-entities": f"5. Create Your Entities",
            "#resolve-entities": f"6. Resolve Entities",
        },
        orientation="vertical",
        ),
        mo.md(f"## {mo.icon('fluent-color:person-20')} User"),
        user_name,
        mo.md(f"## {mo.icon('fluent-color:book-16')} Case"),
        mo.md(f"_{doc.title}_"),
        mo.md(f"## {mo.icon('fluent-color:molecule-16')} Database"),
        run_test_neo4j,
        run_delete_neo4j,
        mo.md(db_line),
        mo.md(f"## {mo.icon('fluent-color:data-line-16')} Language Model"),
        run_test_dspy,
        run_test_genai,
        mo.md(lm_line),
    ])
    return


@app.cell
def _():
    import marimo as mo
    import nest_asyncio


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
        connect_dspy_large,
        connect_dspy_small,
        delete_neo4j
    )
    from neuro_noir.datasets import list_datasets, load_dataset
    from neuro_noir.core.app import Application
    from neuro_noir.models.document import Document

    nest_asyncio.apply()
    app = Application()
    return BaseModel, Field, Optional, app, list_datasets, mo


if __name__ == "__main__":
    app.run()
