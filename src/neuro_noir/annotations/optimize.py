from typing import Optional
import dspy
from dspy.teleprompt.gepa.gepa_utils import DSPyTrace, ScoreWithFeedback

from neuro_noir.annotations.judges import TripleJudge


triple_judge = dspy.ChainOfThought(TripleJudge)


def gepa_metric(
    gold,
    pred,
    trace = None,
    pred_nam = None,
    pred_trace = None,
) -> dspy.Prediction:
    """
    Metric for GEPA:
    - Score in [0, 1] based on overlap of gold vs predicted triples.
    - Textual feedback summarizing matches/mismatches.
    """

    """
    Metric for GEPA that uses a separate LLM judge.

    We don't assume gold.annotations is complete.
    We just ask the judge: how good are pred.annotations
    for this (history, paragraph)?
    """

    history = getattr(gold, "history", gold.get("history", []))
    paragraph = getattr(gold, "paragraph", gold.get("paragraph", ""))
    annotations = getattr(pred, "annotations", []) or []

    judge_out = triple_judge(
        history=history,
        paragraph=paragraph,
        annotations=annotations,
    )

    # make sure score stays in [0, 1]
    score = max(0.0, min(1.0, float(judge_out.score)))
    feedback = judge_out.feedback or "No feedback."

    return dspy.Prediction(score=score, feedback=feedback)


def optimize(llm, student, trainset):
    compiler = dspy.GEPA(
        metric=gepa_metric, # type: ignore 
        reflection_lm=llm,
        track_stats=True,
        track_best_outputs=True,
        # auto="light", 
        max_full_evals=5
    )

    return compiler.compile(student, trainset=trainset)