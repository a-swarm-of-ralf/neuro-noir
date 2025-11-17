import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from neuro_noir.core.config import Settings
    from neuro_noir.chunking.scenebased import SceneBasedChunker
    from neuro_noir.datasets import the_adventure_of_retired_colorman
    return SceneBasedChunker, Settings, the_adventure_of_retired_colorman


@app.cell
def _(SceneBasedChunker, Settings, the_adventure_of_retired_colorman):
    doc = the_adventure_of_retired_colorman()
    settings = Settings()
    chunker = SceneBasedChunker(document=doc, cfg=settings)
    return chunker, doc


@app.cell
def _(chunker):
    chunks = chunker.chunk()
    return (chunks,)


@app.cell
def _(doc):
    print(doc.content[2500:5000])
    return


@app.cell
def _(chunks):
    print(len(chunks[3].content))
    print(chunks[3].content)
    return


@app.cell
def _(chunks, doc):
    for chunk in chunks:
        if chunk.content not in doc.content:
            print(f"Chunk {chunk.id} not found in document!")
    return


if __name__ == "__main__":
    app.run()
