from __future__ import annotations
from importlib.resources import files

def load_dataset(name: str) -> str:
    """Load a dataset by name."""
    return files("neuro_noir.datasets").joinpath(name).read_text(encoding="utf-8")

def the_adventure_of_retired_colorman() -> str:
    """Load 'The Adventure of the Retired Colorman' dataset."""
    return load_dataset("the-adventure-of-the-retired-colourman.txt")

def the_adventure_of_the_three_students() -> str:
    """Load 'The Adventure of the Three Students' dataset."""
    return load_dataset("the-adventure-of-the-three-students.txt")

def the_five_orange_pips() -> str:
    """Load 'The Five Orange Pips' dataset."""
    return load_dataset("the-five-orange-pips.txt")