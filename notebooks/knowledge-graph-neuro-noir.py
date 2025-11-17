import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _(
    mo,
    neo4j_delete_stack,
    neo4j_password,
    neo4j_test_stack,
    neo4j_uri,
    neo4j_user,
):
    mo.md(f"""
    ## Settings
    **Databse Settings**
    {neo4j_uri}
    {neo4j_user}
    {neo4j_password}
    {neo4j_test_stack}
    {neo4j_delete_stack}
    """)
    return


@app.cell
def _(case_stack, mo):
    mo.md(f"""
    ## Select Your Case

    Select your case then press _'Load!'_.
    {case_stack}
    """)
    return


@app.cell
def _(doc, mo):
    if doc:
        case_text_md = f"""
    ### Your Case: '{doc.title}'

    _{doc.paragraphs[1]}_

    **Statistics:** 
    - {len(doc.content)} characters
    - {len(doc.chunks)} chunks
    - {len(doc.paragraphs)} paragraphs
    - {len(doc.annotations)} annotated paragraphs
    """
    else:
        case_text_md = "_no case loaded yet..._"
    mo.md(case_text_md)
    return


@app.cell
def _(doc):
    if doc and len(doc.annotations) > 12:
        doc.annotations[12]
    return


@app.cell
def _(btn_add_episoders, max_episodes, mo):
    mo.md(f"""
    ## Add Episodes

    {max_episodes}
    {btn_add_episoders}
    """)
    return


@app.cell
async def _(cfg):
    from neuro_noir.core.connections import connect_graphiti
    graphiti = await connect_graphiti(cfg)
    return (graphiti,)


@app.cell
async def _(btn_add_episoders, doc, graphiti, max_episodes, mo):
    from neuro_noir.core.database import add_episode

    async def _go(episodes: list[str | dict], doc, db):
        args = {
            "title": doc.title,
            "subtitle": f"Adding {len(episodes)} Episodes...",
            "completion_title": doc.title,
            "completion_subtitle": f"{len(episodes)} Episodes Added!",
            "total": len(episodes)
        }
        results = []
        for idx, episode in mo.status.progress_bar(enumerate(episodes), **args):
            result = await add_episode(db, doc, episode, idx)
            results.append(result)
        return results

    processed_episodes = []
    if btn_add_episoders.value and doc:
        processed_episodes = await _go(doc.annotations[:max_episodes.value], doc, graphiti)
    elif not doc:
        print(f"No document loaded. Please use ''Load' button  under 'Select Your Case'.")
    elif not btn_add_episoders.value:
        print(f"Press 'Add Episodes' in the 'Add Episodes' section to start.")
    return


@app.cell
async def _(graphiti):
    async def search_graph(query: str): 
        results = await graphiti.search(query)

        # Print search results
        print('\nSearch Results:')
        for result in results:
            print(f'UUID: {result.uuid}')
            print(f'Fact: {result.fact}')
            if hasattr(result, 'valid_at') and result.valid_at:
                print(f'Valid from: {result.valid_at}')
            if hasattr(result, 'invalid_at') and result.invalid_at:
                print(f'Valid until: {result.invalid_at}')
            for key, value in result.attributes.items():
                print(f"Attribute '{key}': '{value}'")
            print('---')
        return results

    await search_graph('Who  is the retired color man?')
    return


@app.cell
def _(mo):
    max_episodes = mo.ui.number(start=1, stop=2640, value=10, label="Maximum Number of Episodes to Extract", full_width=True)
    return (max_episodes,)


@app.cell
def _(mo):
    btn_add_episoders = mo.ui.run_button(label="Add Episodes", full_width=True, kind="info")
    return (btn_add_episoders,)


@app.cell
def _():
    import marimo as mo

    from graphiti_core import Graphiti
    from graphiti_core.nodes import EpisodeType
    from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF

    from neo4j import GraphDatabase, exceptions

    import dspy

    from pydantic import BaseModel, Field
    from typing import Optional

    from neuro_noir.core.config import Settings

    cfg = Settings()
    return GraphDatabase, cfg, exceptions, mo


@app.cell
def _(cfg, mo):
    neo4j_uri = mo.ui.text(label="Neo4j URI", value=cfg.NEO4J_URI, full_width=True)
    neo4j_user = mo.ui.text(label="Neo4j User", value=cfg.NEO4J_USERNAME, full_width=True)
    neo4j_password = mo.ui.text(label="Neo4j Password",value=cfg.NEO4J_PASSWORD, kind="password", full_width=True)
    return neo4j_password, neo4j_uri, neo4j_user


@app.cell
def _(mo):
    get_neo4j_msg, set_neo4j_msg = mo.state("Press the 'Test' Button top test connection...")
    return get_neo4j_msg, set_neo4j_msg


@app.cell
def _(mo):
    get_neo4j_del_msg, set_neo4j_del_msg = mo.state("💀💀💀 Warning deleting database is permanent! 💀💀💀")
    return get_neo4j_del_msg, set_neo4j_del_msg


@app.cell
def _(GraphDatabase, exceptions):
    def neo4j_test(uri: str, user: str, pw: str, callback):
        try:
            driver = GraphDatabase.driver(uri, auth=(user, pw))
            with driver.session() as session:
                session.run("RETURN 1").consume()
            driver.close()
            return callback("✅ Connected successfully.")
        except exceptions.Neo4jError as n4je:
            return callback(f"❌ Connection Error: {str(n4je)}.")
        except Exception as e:
            return callback(f"❌ Unexpected Error: {str(e)}.")

    def neo4j_delete(uri: str, user: str, password: str, callback) -> None:
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")

            driver.close()
            callback("✅ Database cleared successfully.")

        except exceptions.Neo4jError as e:
            callback(f"❌ Neo4j error while clearing database: {e}")

        except Exception as e:
            callback(f"❌ Unexpected error while clearing database: {e}")
    return neo4j_delete, neo4j_test


@app.cell
def _(mo, neo4j_password, neo4j_test, neo4j_uri, neo4j_user, set_neo4j_msg):
    neo4j_test_btn = mo.ui.button(on_click=lambda _: neo4j_test(neo4j_uri.value, neo4j_user.value, neo4j_password.value, set_neo4j_msg), label="Test", kind="info")
    return (neo4j_test_btn,)


@app.cell
def _(
    mo,
    neo4j_delete,
    neo4j_password,
    neo4j_uri,
    neo4j_user,
    set_neo4j_del_msg,
):
    neo4j_delete_btn = mo.ui.button(on_click=lambda _: neo4j_delete(neo4j_uri.value, neo4j_user.value, neo4j_password.value, set_neo4j_del_msg), label="Delete", kind="danger")
    return (neo4j_delete_btn,)


@app.cell
def _(get_neo4j_msg, mo):
    neo4j_test_text = mo.ui.text(value=get_neo4j_msg(), disabled=True, full_width=True)
    return (neo4j_test_text,)


@app.cell
def _(get_neo4j_del_msg, mo):
    neo4j_delete_text = mo.ui.text(value=get_neo4j_del_msg(), disabled=True, full_width=True)
    return (neo4j_delete_text,)


@app.cell
def _(mo, neo4j_test_btn, neo4j_test_text):
    neo4j_test_stack = mo.hstack([neo4j_test_btn, neo4j_test_text], widths=[0, 1],)
    return (neo4j_test_stack,)


@app.cell
def _(mo, neo4j_delete_btn, neo4j_delete_text):
    neo4j_delete_stack = mo.hstack([neo4j_delete_btn, neo4j_delete_text], widths=[0, 1],)
    return (neo4j_delete_stack,)


@app.cell
def _(mo):
    from neuro_noir.datasets import list_datasets

    cases_dropdown = mo.ui.dropdown(options=list_datasets(), value="the-adventure-of-the-retired-colourman", full_width=True)
    return (cases_dropdown,)


@app.cell
def _(mo):
    load_case_button = mo.ui.run_button(label="Load!", kind="info")
    return (load_case_button,)


@app.cell
def _(cases_dropdown, load_case_button, mo):
    case_stack = mo.hstack([cases_dropdown, load_case_button], widths=[1, 0],)
    return (case_stack,)


@app.cell
def _(cases_dropdown, load_case_button):
    from neuro_noir.datasets import load_dataset

    if load_case_button.value:
        doc = load_dataset(cases_dropdown.value)
    else: 
        doc = None
    return (doc,)


if __name__ == "__main__":
    app.run()
