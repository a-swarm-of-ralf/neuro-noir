import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import dspy
    from neuro_noir.core.connections import verify_dspy, verify_neo4j, connect_dspy_large, connect_dspy_small, connect_neo4j
    from neuro_noir.core.config import Settings
    from neuro_noir.datasets import load_dataset, list_datasets
    return (
        Settings,
        connect_dspy_large,
        connect_dspy_small,
        dspy,
        load_dataset,
        mo,
        verify_dspy,
        verify_neo4j,
    )


@app.cell
def _(Settings):
    settings = Settings()
    return (settings,)


@app.cell
def _(load_dataset):
    doc = load_dataset("the-adventure-of-the-retired-colourman")
    return (doc,)


@app.cell
def _(doc):
    paragraphs_with_history_30 = doc.rolling_history(window=30)
    paragraphs_with_history_30[4]
    return (paragraphs_with_history_30,)


app._unparsable_cell(
    r"""
    dspy.Example(
        history=[
          \"THE ADVENTURE OF THE RETIRED COLOURMAN\",
          \"Sherlock Holmes was in a melancholy and philosophic mood that morning.\nHis alert practical nature was subject to such reactions.\",
          \"\\"Did you see him?\\" he asked.\",
          \"\\"You mean the old fellow who has just gone out?\\"\"
        ], 
        paragraph=\"\\"Precisely.\\"\"
        annotations=[
        (
            \"<\\"Precisely.\\": Statement>\n\"
            \"<property description: 'Sherlock Holmes confirms to Watson tha he was indeed talking about the old fellow.'>\n\"
            \"<SpokenBy> <\\"Sherlock Holmes\\": Person>\n\"
            \"<SpokenTo> <\\"Dr. John Watson\\": Person>\n\"
            \"<About> <\\"the old fellow\\": Person>\n\"
            \"<InResponseTo> <\\"You mean the old fellow who has just gone out?\\": Statement>\n\"
        ),
        ]
    ).with_inputs(\"history\", \"paragraph\")
    """,
    name="_"
)


@app.cell
def _(settings, verify_neo4j):
    verify_neo4j(settings)
    return


@app.cell
def _(settings, verify_dspy):
    verify_dspy(settings)
    return


@app.cell
def _(connect_dspy_small, settings):
    connect_dspy_small(settings)("Hello? Are you there?")
    return


@app.cell
def _(connect_dspy_large, settings):
    connect_dspy_large(settings)("Hello? Are you there?")
    return


@app.cell
def _(connect_dspy_large, dspy, settings):
    from neuro_noir.annotations.examples import training_examples
    from neuro_noir.annotations.signature import DetectiveAnnotate
    from neuro_noir.annotations.optimize import optimize
    from neuro_noir.annotations.judges import TripleJudge

    connect_dspy_large(settings)
    annotator = dspy.ChainOfThought(DetectiveAnnotate)
    judge = dspy.ChainOfThought(TripleJudge)
    return annotator, judge, optimize, training_examples


@app.cell
def _(annotator, judge, training_examples):
    def _(n):
        return judge(**training_examples[n].inputs(), annotations=annotator(**training_examples[n].inputs()).annotations)

    _(9)
    return


@app.cell
def _(annotator, connect_dspy_small, optimize, settings, training_examples):
    optimized_annotator = optimize(
        llm=connect_dspy_small(settings),
        student=annotator,
        trainset=training_examples,
    )
    return (optimized_annotator,)


@app.cell
def _(optimized_annotator):
    optimized_annotator.save("./data/models/annotator.json", save_program=False)
    return


@app.cell
def _(optimized_annotator, paragraphs_with_history_30):
    optimized_annotator(**paragraphs_with_history_30[51])
    return


@app.cell
def _(optimized_annotator, paragraphs_with_history_30):
    optimized_annotator(**paragraphs_with_history_30[51]).annotations
    return


@app.cell
def _(optimized_annotator):
    print(optimized_annotator.predict.signature.instructions)
    return


@app.cell
def _(doc, mo, optimized_annotator, paragraphs_with_history_30):
    def _():
        results = []
        for paragraph_with_history in mo.status.progress_bar(
            paragraphs_with_history_30, 
            title=f"Annotating {doc.title}...",completion_subtitle=f"Annotated {doc.title}!"):
            result = optimized_annotator(**paragraph_with_history)
            results.append({ "annotations": result.annotations, "reasoning": result.reasoning, **paragraph_with_history})
        return results

    annotated_doc = _()
    return (annotated_doc,)


@app.cell
def _(annotated_doc, doc):
    import json
    import os

    os.makedirs(f"data/{doc.id}", exist_ok=True)
    with open(f"data/{doc.id}/annotations.json", "w") as file:
        json.dump(annotated_doc, file, indent=4)
    return


if __name__ == "__main__":
    app.run()
