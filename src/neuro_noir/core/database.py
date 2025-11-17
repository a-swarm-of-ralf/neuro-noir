
from datetime import datetime, timezone
import json
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

from neuro_noir.graph.mapping import edge_type_map, entity_types, edge_types
from neuro_noir.models.document import Document


async def add_episode(graphiti: Graphiti, doc: Document, episode: str | dict, index: int):
    return await graphiti.add_episode(
        name=f'{doc.title} {index+1:03}',
        episode_body=json.dumps(episode, indent=4) if isinstance(episode, dict) else episode,
        source=EpisodeType.json if isinstance(episode, dict) else EpisodeType.text,
        source_description=doc.title,
        reference_time=datetime.now(timezone.utc),
        group_id=doc.id,
        entity_types=entity_types,
        edge_types=edge_types,
        edge_type_map=edge_type_map,
    )