from google import genai
from google.genai import types


client = genai.Client(
        vertexai=True, project='neologic-9-feb-2026', location='europe-west4'
    )


response = client.models.embed_content(
        model='gemini-embedding-001',
        contents=['why is the sky blue?', 'What is your age?'],  
        config=types.EmbedContentConfig(task_type=TASK_DOC, output_dimensionality=1536)
    )


def embed(idx, chunk):
        if idx != chunk["index"]:
            raise ValueError("Index mismatch")
        if chunk["chunk"]:
            _response = client.models.embed_content(model='gemini-embedding-001',
                contents=chunk["chunk"],  
                config=types.EmbedContentConfig(task_type=TASK_DOC, output_dimensionality=1536)
            )
            chunk["embedding"] = _response.embeddings[0].values
        else:
            chunk["embedding"] = []
        if chunk["statements"]:
            _response = client.models.embed_content(model='gemini-embedding-001',
                contents=[st["sentence"] for st in chunk["statements"]],  
                config=types.EmbedContentConfig(task_type=TASK_DOC, output_dimensionality=1536)
            )
            _embeddings = [ emb.values for emb in _response.embeddings]
            for st, emb in zip(chunk["statements"], _embeddings):
                st["embedding"] = emb
        else:
            for st in chunk["statements"]:
                st["embedding"] = []
        return chunk


max_n = 691
for idx in range(max_n):
    print(f"Reading file {idx + 1}/{max_n}")
    with open(STATEMENTS_FILE.format(idx=idx), "r", encoding="utf-8") as _statements_fp:
        _chunk_data = json.load(_statements_fp)
    _chunk_with_embed = embed(idx, _chunk_data)
    print(f"Writing file {idx + 1}/{max_n}")
    with open(EMBED_FILE.format(idx=idx), "w", encoding="utf-8") as _embed_fp:
        _chunk_with_embed = json.dump(_chunk_with_embed, _embed_fp)