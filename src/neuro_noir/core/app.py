from typing import Callable
from graphiti_core import Graphiti
from neuro_noir.core.config import Settings
from neuro_noir.core.database import Database
from neuro_noir.models.chunk import Chunk
from neuro_noir.models.document import Document


class Application:
    
    def __init__(self):
        self.config = Settings()
        self.graph = Database(self.config)

    async def initialize(self):
        await self.graph.initialize()

    async def clear(self):
        await self.graph.clear()

    def register_chunker(self, chunker: Callable[[Document], list[Chunk]]):
        self.chunker = chunker