import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import marimo as mo
    from google import genai
    from google.genai import Client
    import dspy

    return dspy, genai, os


@app.cell
def _(os):
    print(f"GOOGLE_GENAI_USE_VERTEXAI: {os.getenv('GOOGLE_GENAI_USE_VERTEXAI')}")
    print(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
    print(f"GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")
    print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')}")
    return


@app.cell
def _(genai):
    client = genai.Client(
        vertexai=True,
        project="semantic-bank", # Replace with your actual GCP project ID
    )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents="Responed with 'Connected'."
    )
    print(response.text)
    return


@app.cell
def _(dspy):
    lm = dspy.LM(
        "vertex_ai/gemini-2.5-pro",
        vertex_project="semantic-bank",
        cache=True
    )
    dspy.configure(lm=lm)
    return (lm,)


@app.cell
def _(lm):
    lm("Responed with 'Connected'.")[0]
    return


if __name__ == "__main__":
    app.run()
