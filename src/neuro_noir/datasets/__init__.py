from __future__ import annotations
from importlib.resources import files

import json

from neuro_noir.models.document import Document

def list_datasets() -> list[str]:
    """List available datasets."""
    dataset_dir = files("neuro_noir.datasets")
    return [item.name for item in dataset_dir.iterdir() if item.is_dir() and not item.name.startswith("__")]

def load_content(name: str) -> str:
    """Load a dataset by name."""
    return files("neuro_noir.datasets").joinpath(name, "content.txt").read_text(encoding="utf-8")

def load_annotations(name: str) -> list[dict[str, str]]:
    """Load annotations for a dataset by name."""
    annotations_text = files("neuro_noir.datasets").joinpath(name, "annotations.json").read_text(encoding="utf-8")
    annotations = json.loads(annotations_text) if annotations_text.strip().startswith("[") else []
    if annotations and len(annotations) > 0 and "fragment" in annotations[0]:
        annotations = [{ "annotation": rec["annotation"], "paragraph": rec["fragment"]} for rec in annotations]
    return annotations

def load_dataset(name: str) -> Document:
    """Load a dataset by name."""
    text = load_content(name)
    annotations = load_annotations(name)
    title = name.replace("-", " ").title()
    return Document(id=name, title=title, content=text, annotations=annotations)

def the_adventure_of_retired_colorman() -> Document:
    """Load 'The Adventure of the Retired Colorman' dataset."""
    text =  load_content("the-adventure-of-the-retired-colourman")
    annotations = load_annotations("the-adventure-of-the-retired-colourman")
    return Document(id="the-adventure-of-the-retired-colorman", title="The Adventure of the Retired Colorman", content=text, annotations=annotations)

def the_adventure_of_the_three_students() -> Document:
    """Load 'The Adventure of the Three Students' dataset."""
    text = load_content("the-adventure-of-the-three-students")
    annotations = load_annotations("the-adventure-of-the-three-students")
    return Document(id="the-adventure-of-the-three-students", title="The Adventure of the Three Students", content=text, annotations=annotations)

def the_five_orange_pips() -> Document:
    """Load 'The Five Orange Pips' dataset."""
    text = load_content("the-five-orange-pips")
    annotations = load_annotations("the-five-orange-pips")
    return Document(id="the-five-orange-pips", title="The Five Orange Pips", content=text, annotations=annotations)

def the_mysterious_affair_at_styles() -> Document:
    """Load 'The Mysterious Affair at Styles' dataset."""
    text = load_content("the-mysterious-affair-at-styles")
    annotations = load_annotations("the-mysterious-affair-at-styles")
    return Document(id="the-mysterious-affair-at-styles", title="The Mysterious Affair at Styles", content=text, annotations=annotations)