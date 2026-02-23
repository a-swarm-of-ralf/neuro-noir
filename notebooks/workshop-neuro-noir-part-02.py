import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    # Workshop Neuro-Noir Part 2

    This is part 2 of the Neuro-Noir workshop series.

    ![image of tools](public/tools.jpg)

    ## Introduction

    In Part 1, you built the foundation: a structured knowledge graph enriched with embeddings, entities, and resolved references. You transformed unstructured narrative text into a machine-readable representation of facts and evidence.

    In this second part, we focus on what comes next: **using that structured knowledge to reason, investigate, and make decisions**. You will learn how to build AI agents that do not merely retrieve information, but actively think with it—querying the graph, evaluating hypotheses, and explaining their conclusions step by step.

    Here, the knowledge graph becomes more than a database. It becomes the **working memory** of an intelligent investigator.

    ---

    /// details | Why Neurosymbolic AI in Part 2?
        type: info

    In Part 1, neural models helped you extract structure from text. In Part 2, symbolic reasoning takes center stage.

    Most LLM-based applications stop at “retrieve and summarize.” They fetch relevant passages and generate a plausible answer. While useful, this approach offers little control over *how* conclusions are reached.

    **Neurosymbolic AI** goes further by combining:

    - **Neural systems** for language understanding and interpretation.
    - **Symbolic systems** for querying graphs, enforcing constraints, and applying logical rules.

    In this part of the workshop, your knowledge graph becomes the backbone of reasoning. Instead of guessing, your agent must consult evidence, test assumptions, and justify its decisions using explicit steps.

    ///

    /// details | From Knowledge Graph to Investigator
        type: info

    By now, your graph contains:

    - Statements extracted from the story
    - Linked entities and relationships
    - Resolved references and disambiguated concepts
    - Embedded representations for semantic search

    In Part 2, you will learn how to *use* this structure.

    Your agent will:

    - Search the graph for relevant evidence
    - Compare competing hypotheses
    - Check alibis, timelines, and contradictions
    - Update conclusions when new facts appear

    Rather than producing a single answer, the system will behave like a careful investigator—gathering facts, weighing alternatives, and revising its beliefs.

    ///

    /// details | What You’ll Learn
        type: info

    By the end of this part of the workshop, you will:

    - Understand how to turn a knowledge graph into an active reasoning system.
    - Learn how to:
      - Build graph-aware tools for LLM agents.
      - Design structured reasoning steps.
      - Combine retrieval, symbolic constraints, and LLM reasoning.
    - Create an agent that:
      - Queries Neo4j effectively.
      - Evaluates suspects based on evidence.
      - Explains its reasoning in human-readable form.
    - Explore how to move from “RAG-style answers” to **multi-step, inspectable decision-making pipelines**.

    You will see how LLMs can function as reasoning components inside a larger system, rather than as isolated oracles.

    ///

    /// details | “Why not just use RAG and a chat prompt?”
        type: info

    A standard RAG system can retrieve relevant chunks and generate a convincing answer. For many applications, that is sufficient.

    But RAG alone cannot easily:

    - Enforce logical constraints
    - Track evolving hypotheses
    - Detect contradictions
    - Explain why alternatives were rejected
    - Re-evaluate conclusions when data changes

    In this workshop, you go beyond “search and summarize.”

    You build systems that provide:

    - **Traceability**: Every conclusion is backed by explicit facts.
    - **Consistency**: Rules and constraints are applied systematically.
    - **Adaptability**: New evidence changes outcomes.
    - **Accountability**: Reasoning can be inspected and audited.

    These properties are essential in domains like investigations, compliance, fraud detection, and safety-critical decision systems.

    An LLM can guess.
    Your agent will reason.

    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Contents

    1. **Test Settings**  
       Verify your connections to the graph database and language model.

    2. **Build Basic Graph Tools**  
       Create simple tools that retrieve entities, statements, and chunks from the knowledge graph.

    3. **Create Advanced Query Tools**  
       Extend your tools with semantic search, multi-hop queries, and filtered retrieval.

    4. **Assemble Evidence Context**  
       Combine the outputs of multiple tools into a coherent “case file” that represents the current state of evidence.

    5. **Design Reasoning Steps**  
       Define structured reasoning procedures for evaluating alibis, motives, timelines, and contradictions.

    6. **Build the Investigation Agent**  
       Integrate tools and reasoning into an autonomous agent that can analyze the case and explain its conclusions.

    /// attention | Run the Notebook!

    Start by running the entire notebook using the {mo.icon('lucide:circle-play')} button in the bottom right.  
    This enables all interactive UI elements and prepares the environment for the exercises.
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
    mo.md(r"""
    ## Building Basic Graph Tools

    In this section, we begin turning your knowledge graph into something an AI system can actively use. Rather than querying Neo4j manually, you will build a small collection of reusable **tools** that expose common graph operations in a clean, consistent way. These tools form the foundation on which all later reasoning and agent behavior will be built.

    By the end of this section, you will have a set of well-defined functions that allow an agent to retrieve entities, statements, and evidence from the graph in a controlled and predictable manner.

    /// details | What Are “Tools”?
        type: info
    In this workshop, a **tool** is a function that:

    - Takes structured input (IDs, names, filters, queries)
    - Performs a well-defined operation on the knowledge graph
    - Returns structured, predictable output

    From the agent’s perspective, tools are its way of “interacting with the world.”
    An agent cannot directly see your database. It can only call tools and reason about their results.

    In other words:

    - The **knowledge graph** is the memory
    - The **tools** are the senses and hands
    - The **agent** is the reasoning system

    Well-designed tools determine what the agent is capable of perceiving and acting upon.
    ///

    /// details | Best Practices for Writing Tools
        type: info
    When designing tools for agents, clarity and reliability matter more than cleverness.

    Keep the following principles in mind:

    **1. Do One Thing Well**
    Each tool should have a single, clear purpose. Avoid “do-everything” functions that mix multiple responsibilities.

    **2. Use Explicit Inputs and Outputs**
    Inputs should be **simple** and **well-defined**. Outputs should follow a consistent structure that is easy for both humans and agents to interpret.

    **3. Handle Missing Data Gracefully**
    Tools should return empty results or clear error messages instead of failing silently.

    These principles help prevent fragile pipelines and make later reasoning steps much more robust.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Implement Basic Graph Tools

    In this exercise, you will implement a set of simple tools for interacting with your knowledge graph. To implement these features you can use the methods on the `app`object in this notebook.

    - `app.embed(txt: str) -> list[float]` creates an embedding
    - `app.find_chunk(embedding: list[float]) -> list[Chunk]` gives the closest _n_ chunks
    - `app.find_statement(embedding: list[float]) -> list[Statement]` gives the closest _n_ statements
    - `app.find_entity(embedding: list[float]) -> list[Entity]` gives the closest _n_ entities
    - `app.cypher_query(cypher_query: str) -> list[dict]` executes a cypher query directly on the neo4j database

    /// admonition | Exercise 1

    Below are three skeletons for tools. Complete these tools so

    - `search` does a free search of the graph
    - `search_entities` does a narrow search for enties on the name
    - `seach_statements` retrieves all statements assosiated with an entity

    ///

    Take your time to design them carefully. Well-written tools here will make everything that follows easier.
    """)
    return


@app.cell
def _(app):
    def search(query: str) -> str:
        """
        Query the knowledge graph to find related chunks.
        """
        # return "no results :("
        print(f"Searching for Chunk '{query}'")
        emb = app.embed(query)
        return "\n\n".join([f"### Chunk {item.index} [score={score}]\n\n{item.content}" for item, score in app.find_chunk(embedding=emb)])


    def search_entities(query: str) -> str:
        """
        Query the knowledge graph to find related entities.
        """
        # return "no results :("
        print(f"Searching for Entity '{query}'")
        emb = app.embed(query)
        return "\n\n".join([f"### Entity {item.name} [score={score}]\n\n{item.model_dump_json(exclude={'name_embedding', 'profile_embedding'})}" for item, score in app.find_entity(embedding=emb)])

    def search_statements(query: str) -> str:
        """
        Query the knowledge graph to find related statements.
        """
        # return "no results :("
        print(f"Searching for Statement '{query}'")
        emb = app.embed(query)
        return "\n\n".join([f"### Statement {item.subject}-{item.predicate}-{item.object_} [score={score}]\n\n{item.model_dump_json(exclude={'name_embedding', 'profile_embedding'})}" for item, score in app.find_statement(embedding=emb)])

    return search, search_entities, search_statements


@app.cell
def _():
    # mo.md(search("Amberly"))
    return


@app.cell
def _():
    # mo.md(search_entities("Amberly"))
    return


@app.cell
def _():
    # mo.md(search_statements("Amberly"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating Advanced Tools

    In the previous section, you built basic tools that expose simple, direct queries to the knowledge graph. These tools are sufficient for retrieving individual facts, but real investigations rarely depend on single, isolated pieces of information. Advanced tools on the other hand are about navigating the graph. Traversal is an essential component of symbolic reasoning. It can answer questions like how are entity X and entity Y connected.

    /// details | Combining Structure and Semantics
        type: info
    Your knowledge graph contains two complementary forms of information:

    - **Symbolic structure**: nodes, relationships, labels, and constraints
    - **Semantic representations**: embeddings that capture meaning and similarity

    Advanced query tools bridge these two worlds.

    For example, a tool may:

    - Use vector search to find relevant chunks
    - Traverse relationships to collect related entities
    - Apply logical filters to remove irrelevant results
    - Rank evidence by relevance or confidence

    This hybrid approach is what allows agents to move beyond keyword matching and perform context-aware retrieval.

    ///

    /// details | Keeping it Safe
        type: info
    As tools become more expressive, it becomes more important to control their behavior.

    When writing advanced query tools, aim for:

    **1. Clear Intent**
    Each tool should correspond to a recognizable investigative question.

    **2. Bounded Output**
    Limit result sizes and scope to prevent overwhelming the agent.

    **3. Predictable Structure**
    Return results in consistent, documented formats.

    **4. Defensive Filtering**
    Exclude low-quality, ambiguous, or irrelevant data where possible.

    **5. Performance Awareness**
    Complex queries can be expensive. Design them to scale.

    These practices help ensure that increased power does not lead to instability.

    ///

    /// details | What can we do with advanced tools?
        type: info
    Think of advanced query tools as “macro-operations” built on top of basic primitives.

    They encapsulate common investigative patterns and make them reusable:

    - Timeline reconstruction
    - Evidence comparison
    - Hypothesis validation
    - Similarity-based retrieval
    - Contradiction detection

    By packaging these patterns into tools, you simplify the reasoning layer and reduce the burden on the agent.

    ///

    /// admonition | Exercise 2

    Below are two skeletons for more advance tools. Complete these tools so

    - `connected`: Given two entities return how they are connected in the graph.
    - `related`: Given an entity find all related entities.

    ///
    """)
    return


@app.cell
def _():
    def connected(entity1: str, entity2: str) -> str:
        """
        Find the shortest path between entity1 and entity2.

        Returns:
            str: The shortest path found between entity1 and entity2.
        """
        return "I refuse!"

    def related(entity: str) -> list[str]:
        """
        Find all entities that are related to the specified entity.
        """
        return "I don';t want to know you!"

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## From Facts to Knowledge

    In the previous section, you built a collection of tools that allow an agent to retrieve individual pieces of information from the knowledge graph. While these tools are powerful, each one only provides a small, isolated view of the case.

    To keep thing more coherent we allow the agent to create new node and assoiations. Then it can build up a context and remmeber deductions it made.

    /// details | Isn't that dangerous?
        type: info

    Yes!

    Language models are by their very nature unpredictable. Allowing them to make actual changes to you data or files can lead to destrcutive results.

    In this context we mitigate it by allowing the agent to only add, and by only allowing to maipulate certain type of nodes. We introduce a Evidence type for this. So our entities and statements are safe while the agent creates and links just evidence nodes. Furthermore retraction does not involve deletion but adding invalidation data to the evidence, so the agent can only add, never remove data.

    ///

    /// admonition | Exercise 3

    Create the following tools for our agent. These tools require adding nodes and there inputs are more complex than before.

    - `assert_evidence`: Create new evidence node.
    - `retract_evidence`: Invalidate evidence node.

    ///
    """)
    return


@app.cell
def _():
    def assert_evidence(name: str, description: str, derived_from: str, explanation: str) -> str:
        """
        Creates a new evidence node linked to the 'derived_from' node.
        """
        return "You can't proof anything!"

    def retract_evidence(name: str, explanation: str) -> str:
        """
        Invalidates an existing evidence node.
        """
        return "No Mister Bond, I expect you to die."

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reasoning

    Up until now we created tools that access and manipulate the knowledge graph. That we created these tools and given them to our agent does not mean the agent knows how to use them effectively. Reasoning tools provide the guidance the agent need to create plans to test for the answer. In other words, thereason provides the rules that govern hypotheis testing and validation.

    Think questions like:

    - Who had motive, means, and opportunity?
    - Which alibis are consistent with the timeline?
    - Which statements contradict each other?
    - What assumptions are still unverified?

    /// details | Common Reasoning Patterns
        type: info

    In this workshop, you will work with several recurring patterns, such as:

    - **Hypothesis generation**: Proposing possible suspects or explanations
    - **Constraint checking**: Eliminating candidates that violate known facts
    - **Evidence weighting**: Prioritizing stronger or more reliable statements
    - **Contradiction detection**: Identifying incompatible claims
    - **Belief revision**: Updating conclusions when new evidence appears

    These patterns form the backbone of many real-world analytical systems.
    ///


    /// details | Hybrid Tools
        type: info

    The agent is powered by a large language model. The tools we have created up until now
    have not used any models (except teh embbedings). Many of the task we want to do in
    this step can be done with pure reasoning, but sometimes can also benfit from a
    limited scope agent in itsself.

    Bridging inputs and outputs between a rule engine to actually perform the reasoning
    could be a hybrid task for example.
    ///


    /// details | Reasoning Loop
        type: info

    In symbolic AI reasoning follows specific patterns depending on the exact task at hand. In
    this case it would follow the diagnose pattern. This pattern has a reasoning loop consiting
    following steps:

    - **Hypotheses Selection**
    - **Test Selection**
    - **Test Evaluation**
    - **Hypotheses Evaluation**

    These step are ussually executed in oder in a loop. Sometimes this also include **Hypothesis Generation**, **Test Generation**, and **Conclusion** as extra steps.

    ///

    /// admonition | Exercise 4

    Create the the tools to perform the reasoning loop.

    - `generate_hypotheses`: Generate possible hypothesis
    - `select_hypothesis`:
    - `generate_tests`:
    - `select_test`:
    - `evaluate_test`:
    - `evaluate_hypothesis`:

    ///
    """)
    return


app._unparsable_cell(
    """
    def generate_hypotheses() -> list[str]:
        \"\"\"
        \"\"\"
        return \"It's just a theory.\"

    def select_hypothesis(hypothesis: str) -> list[str]:
        \"\"\"
        \"\"\"
        return \"It's just a theory.\"

    def generate_tests(hypothesis: str) -> str:
        \"\"\"
        \"\"\"
        rerurn \"Tests, tests, always tests!\"

    def select_test(hypothesis: str, test: str, why: str) -> str:
        \"\"\"
        \"\"\"
        return \"Well it measures, ... something...\"

    def evaluate_test(hypothesis: str, test: str) -> str:
        \"\"\"
        \"\"\"
        return \"Mainstream scientists are not addressing the issues.\"

    def evaluate_hypothesis(hypothesis: str, how: str) -> str:
        \"\"\"
        \"\"\"
        return \"Mainstream scientists are not addressing the issues.\"
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Building the Investigation Agent

    In the previous sections, you designed tools for accessing the knowledge graph, assembled structured evidence contexts, and implemented explicit reasoning steps. Each of these components is powerful on its own. In this final section, you will integrate them into a coherent, autonomous **investigation agent**.

    This agent will be able to plan its actions, gather evidence, apply reasoning procedures, and explain its conclusions. Rather than executing predefined scripts, it will dynamically decide which tools to use and how to combine their outputs to solve a case.

    Here, your system becomes more than a collection of functions—it becomes an intelligent workflow.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Assemble the Investigation Agent

    Below you see a piece of skeleton code that defines a minimal agent interface. At this point, you have already built tools, evidence assembly logic, and reasoning procedures. The final step is to combine these components into a functioning investigation agent.

    In this section, you will transform this bare-bones structure into a system that can actively explore the knowledge graph, evaluate evidence, and justify its conclusions. This is where all previous work comes together.

    /// admonition | Exercise 5

    Complete the investigation agent by performing the following steps:

    - Write clear instructions that define the agent’s role, goals, and reasoning style.
    - Design the signature for the reasoning loop, including how the agent uses history and intermediate results.
    - Integrate the tools you created in earlier sections.

    ///

    Test your agent on a full mystery case and inspect how it selects tools, updates its beliefs, and arrives at a conclusion.
    """)
    return


@app.cell
def _(dspy, search, search_entities, search_statements):
    class InvestigationAgent(dspy.Signature):
        """
        You are a keen detective trying to solve a case described in the knowledge graph.

        You can access the knowledge graph through the tools:
        - search: searches for chunks of text given a query
        - search_entities: searches entitities (persons, locations, organisations, ect) given a query
        - search_statements: searches for triples or statements from the text given a query.

        Instructions
        ------------

        - If somebody asks to solve a crime first try to find out about the crime by searching for statements about it. Try different related querys.
        - Given the statements try to find all the entities mentioned in the most relevant statements
        - Then try to find the chunk where the suspect is mentioned based on the get the concusion of the story.
        - Finally answer the question in by first explaining what statements and entiteis you examined and how it led you
          to the conclusion. Only then give the actual answer.

        Output
        ------

        Give the answer as a markdown string
        """
        question: str = dspy.InputField()
        history: dspy.History = dspy.InputField()
        answer: str = dspy.OutputField(desc="A markdown string containing the answer")

    agent = dspy.ReAct(InvestigationAgent, tools=[search, search_entities, search_statements])
    return (agent,)


@app.cell
def _(agent, dspy, mo):
    _history = dspy.History(messages=[])
    mo.md(agent(question="Who murdered mr. Amberly's wife?", history=_history).answer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Chat UI

    /// admonition | Exercise 6.

    Integrate your agent with the chat ui skelton in the cell below.

    ///
    """)
    return


@app.cell
def _(agent, dspy, mo):
    def my_agent_model(messages, config) -> str:
        # Each message has a 
        # - `content` with the message text
        # - `role` with one of ("user", "system", "assistant");
        # Return a string with the message to show in the chat

        # your agent logic here

        # return "I know nothing. I'm innocent!"
        """
        messages: list of {role, content}
        config: marimo config (usually unused)
        """
        print("Agent reasoning...")
        for msg in messages:
            print(f"  - Message: {msg}")

        if not messages:
            print("No Message!")
            return "Please ask me a question."
        
        last = messages[-1]
        print(f"  # Last Message: {last}")
        print(f"  # Last Content: '{last.content}'")
        question = last.content

        history = dspy.History(messages=[ { 'content': msg.content, 'role': msg.role } for msg in messages])

        result = agent(
            question=question,
            history=history,
        )
        print(f"Result: {result}")
        return result.answer

    chat = mo.ui.chat(my_agent_model)

    chat
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
        run_load_case,
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
def _(app, do_the_chunking, run_chunk_case, user_name):
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
    return


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
    return


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
            "#implement-basic-graph-tools": f"1. Implement Basic Graph Tools",
            "#creating-advanced-tools": f"2. Creating Advanced Tools",
            "#from-facts-to-knowledge": f"3. From Facts to Knowledge",
            "#reasoning": f"4. Reasoning",
            "#assemble-the-investigation-agent": f"5. Assemble Agent",
            "#chat-ui": f"6. Chat UI",
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
    return app, dspy, list_datasets, mo


if __name__ == "__main__":
    app.run()
