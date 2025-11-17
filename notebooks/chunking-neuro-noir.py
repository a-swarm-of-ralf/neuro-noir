import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _(cfg):
    import dspy

    lm = dspy.LM(cfg.MODEL_NAME, temperature=1.0, max_tokens=32000)
    dspy.configure(lm=lm)
    return (dspy,)


@app.cell
def _(doc4, mo):
    # Select a Document (Story)
    doc = doc4

    mo.md(f"Selected the Story *'{doc.title}'* to process...")
    return (doc,)


@app.cell
def _(doc, extract_fragements, mo):
    fragments = extract_fragements(doc.content)

    history_and_fragments = [fragments[:i] for i in range(1, len(fragments) + 1)]

    mo.md(f"""
    ### Extracting Fragments From *'{doc.title}'*

    #### Extracted {len(fragments)} fragments.
    - **Smallest** fragement is {min(len(f) for f in fragments)} characters.
    - **Biggest** fragement is {max(len(f) for f in fragments)} characters.
    - **Average** fragement is {round(sum(len(f) for f in fragments) / len(fragments), 1)} characters.

    #### Characteristics
    - {sum(1 for f in fragments if len(f) > 800)} fragements with more than 800 characters.
    - {sum(1 for f in fragments if len(f) > 1000)} fragements with more than 1000 characters.
    - {sum(1 for f in fragments if len(f) > 1200)} fragements with more than 1200 characters.
    - {sum(1 for f in fragments if len(f) > 1400)} fragements with more than 1400 characters.
    - {sum(1 for f in fragments if len(f) > 1500)} fragements with more than 1500 characters.

    #### Smallest fragment
    {[f for f in fragments if len(f) < 6][0]}

    #### Largest fragement
    {[f for f in fragments if len(f) > 1000][0]}
    """)
    return (history_and_fragments,)


@app.cell
def _(history_and_fragments):
    the_ah_fragement = [hf for hf in history_and_fragments if hf[-1] == '“No.”'][0]

    for f in the_ah_fragement[-10:]:
        print(f)
        print()

    print(len(the_ah_fragement))
    return (the_ah_fragement,)


@app.cell
def _(dspy):
    class Annotator(dspy.Signature):
        """
        Annotate a fragement of a story with content needed to understand the fragment.
        The annotation should make clear:
        - Who is speaking
        - Who is adressed
        - What is the topic
        - Where are they
        Derive these from the history. If it is clear from the fragment itself there is nio need to annotate it.
        """

        history: list[str] = dspy.InputField(description="The parts of the story, in order, that came before.")
        fragment: str = dspy.InputField(description="The fragement; a small part of a story or text.")
        annotation: str = dspy.OutputField(description="The annotation that helps understand the fragement.")

    class ChunkByScene(dspy.Signature):
        """
        Group the segments into coherent scenes by listing the segement index where a new scene starts.
        """
        segments: list[str] = dspy.InputField(description="The list of segements or paragraphs that make up the whole story.")
        segement_indexes: list[int] = dspy.OutputField(description="A list of indexes where new scenes start.")

    class SceneScore(dspy.Signature):
        """Judge if this is a coherent scene from a bigger story?"""
        scene: str = dspy.InputField(description="The full text of the scene.")
        score: float = dspy.OutputField(description="How likely is it that this scene is a a complete, ceherent, full scene from a bigger story?")
        feedback: str = dspy.OutputField()

    return Annotator, ChunkByScene


@app.cell
def _(Annotator, dspy):
    annotator = dspy.ChainOfThought(Annotator)
    # annotator = dspy.Predict(Annotator)
    return (annotator,)


@app.cell
def _(annotator, mo, the_ah_fragement):
    response = annotator(history=the_ah_fragement[-20:-1], fragment=the_ah_fragement[-1])

    mo.md(f"""
    #### Sample

    **Fragment**<br>
    "{the_ah_fragement[-1]}"

    **Annotation**<br>
    {response.annotation}
    """)
    return


@app.cell
def _(annotator, history_and_fragments, mo, n):
    import random

    fragments_in_history = 30
    seed = 273
    result = []

    for history_and_fragment in mo.status.progress_bar(history_and_fragments, title=f"Annotating {len(history_and_fragments)} Fragments...",  completion_title=f"Annotated {len(history_and_fragments)} Fragments."):
        annotator_response = annotator(history=history_and_fragment[-n:-1], fragment=history_and_fragment[-1])
        result.append((history_and_fragment[-1], annotator_response.annotation))

    random.seed(seed)
    fragment1, annotation1 = random.choice(result)
    fragment2, annotation2 = random.choice(result)
    fragment3, annotation3 = random.choice(result)
    fragment4, annotation4 = random.choice(result)

    mo.md(f"""
    ## Samples

    ### Sample 1

    **Fragment**<br>
    "{fragment1}"

    **Annotation**<br>
    {annotation1}

    ### Sample 2

    **Fragment**<br>
    "{fragment2}"

    **Annotation**<br>
    {annotation2}

    ### Sample 3

    **Fragment**<br>
    "{fragment3}"

    **Annotation**<br>
    {annotation3}

    ### Sample 4

    **Fragment**<br>
    "{fragment4}"

    **Annotation**<br>
    {annotation4}
    """)
    return (result,)


@app.cell
def _(doc, result):
    import json

    def save_json(data: list[tuple[str, str]]):
        with open(f"data/annotations-{doc.id}.json", mode="w") as file:
            json.dump([{"annotation": anno, "fragment": frag} for (frag, anno) in data], file, indent=4)

    save_json(result)
    return


@app.cell
def _(ChunkByScene, dspy):
    chunker = dspy.ChainOfThought(ChunkByScene)
    return (chunker,)


@app.cell
def _(chunker, doc1, doc2, doc3):
    segments1 = doc1.content.split("\n\n")
    segments2 = doc2.content.split("\n\n")
    segments3 = doc3.content.split("\n\n")
    resp1 = chunker(segments=segments1)
    resp2 = chunker(segments=segments2)
    resp3 = chunker(segments=segments3)
    return resp1, resp2, resp3, segments1, segments2, segments3


@app.cell
def _(resp1, resp2, resp3, segments1, segments2, segments3):
    def extract_scene(res, segments):
        result = []
        last_index = 0
        for index in res.segement_indexes:
            result.append(segments[last_index:index])
            last_index = index
        result.append(segments[last_index:])
        return result

    scenes1 = extract_scene(resp1, segments1)
    scenes2 = extract_scene(resp2, segments2)
    scenes3 = extract_scene(resp3, segments3)
    return scenes1, scenes2, scenes3


@app.cell
def _(doc1, doc2, doc3, scenes1, scenes2, scenes3):
    def scene_stats(scenes, doc):
        title = f"Doc: {doc.title}"
        print()
        print(title)
        print("=" * len(title))
        print(f"  Characters: {len(doc.content)}")
        print(f"  Characters in scenes: {sum([len(seg) for scene in scenes for seg in scene])}")
        for i, scene in enumerate(scenes):
            print(f"    {i}. Scene {i+1}/{len(scenes)} - {len(scene)} segements - {sum(len(seg) for seg in scene)} characters")

    scene_stats(scenes1, doc1)
    scene_stats(scenes2, doc2)
    scene_stats(scenes3, doc3)
    return


@app.cell
def _(scenes3):
    n = 4
    print(scenes3[n][0])
    print("...")
    print(scenes3[n][-1])
    print()
    print()
    print(scenes3[n+1][0])
    print("...")
    print(scenes3[n+1][-1])
    return (n,)


@app.cell
def _(scenes3):
    for seg in scenes3[5]:
        print(seg)
        print("\n")
    return


@app.cell
def _(doc1):
    print(doc1.content[:3000] )
    return


@app.cell
def _(scenes1):
    print(scenes1[4])
    return


@app.cell
def _(dspy):
    examples = [
        dspy.Example(scene="This is a question?", score=0.0, feedback="")
    ]
    return


@app.cell
def _():
    import marimo as mo
    from neuro_noir.datasets import the_five_orange_pips, the_adventure_of_the_three_students, the_adventure_of_retired_colorman, the_mysterious_affair_at_styles
    from neuro_noir.core.config import Settings

    cfg = Settings()

    doc1 = the_five_orange_pips()
    doc2 = the_adventure_of_the_three_students()
    doc3 = the_adventure_of_retired_colorman()
    doc4 = the_mysterious_affair_at_styles()

    def extract_fragements(text: str) -> list[str]:
        return [fragment.strip() for fragment in text.split("\n\n")]
    return cfg, doc1, doc2, doc3, doc4, extract_fragements, mo


if __name__ == "__main__":
    app.run()
