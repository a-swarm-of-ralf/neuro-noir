import dspy


llm = dspy.LM(
                "vertex_ai/gemini-2.5-pro",
                vertex_project="neologic-08-feb-2026",
                vertex_location="europe-west4",
                cache=True,
            )


dspy.configure(lm=llm)