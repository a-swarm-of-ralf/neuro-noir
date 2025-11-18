from typing import Callable
from neuro_noir.core.config import Settings
from neuro_noir.models.document import Document
from neuro_noir.datasets import the_adventure_of_retired_colorman, load_dataset


class Application:
    
    def __init__(self):
        self.cfg = Settings()
        self.doc = the_adventure_of_retired_colorman()

    def load_document(self, key: str) -> Document:
        self.doc = load_dataset(key)
        return self.doc