
from datetime import datetime, timezone
import json
from typing import Type
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from pydantic import BaseModel

from neuro_noir.graph.mapping import edge_type_map, entity_types, edge_types
from neuro_noir.models.document import Document


async def add_episode(graphiti: Graphiti, doc: Document, episode: str | dict, index: int, 
                      entities: dict[str, Type[BaseModel]] | None = None, 
                      edges: dict[str, Type[BaseModel]] | None = None, 
                      edge_map: dict[tuple[str, str], list[str]] | None = None):
    if entities is None:
        entities = entity_types
    if edges is None:
        edges = edge_types
    if edge_map is None:
        edge_map = edge_type_map
    return await graphiti.add_episode(
        name=f'{doc.title} {index+1:03}',
        episode_body=json.dumps(episode, indent=4) if isinstance(episode, dict) else episode,
        source=EpisodeType.json if isinstance(episode, dict) else EpisodeType.text,
        source_description=doc.title,
        reference_time=datetime.now(timezone.utc),
        group_id=doc.id,
        entity_types=entities,
        edge_types=edges,
        edge_type_map=edge_map,
    )