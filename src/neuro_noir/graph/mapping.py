# =========================
# ENTITY TYPE REGISTRY
# =========================

from neuro_noir.graph.entities import Event, Evidence, Location, Object, Organization, Person, Statement
from neuro_noir.graph.relations import Alibi, EvidenceLink, Means, Motive, Opportunity, Presence, StatementAttribution, StatementReference, StatementResponse, Suspicion


entity_types = {
    # Core detective domain entities
    "Person": Person,
    "Statement": Statement,
    "Location": Location,
    "Event": Event,
    "Object": Object,
    "Evidence": Evidence,
    "Organization": Organization,
}


# =========================
# EDGE / RELATION TYPE REGISTRY
# =========================

edge_types = {
    # Person ↔ Statement
    "StatementAttribution": StatementAttribution,  # Person -> Statement

    # Statement ↔ Statement
    "StatementResponse": StatementResponse,        # Statement -> Statement
    "StatementReference": StatementReference,      # Statement -> (Person/Event/Location/Object/Evidence/Organization/Statement)

    # Person ↔ Event (motive, alibi, opportunity, suspicion, presence)
    "Motive": Motive,
    "Alibi": Alibi,
    "Opportunity": Opportunity,
    "Presence": Presence,
    "Suspicion": Suspicion,

    # Object/Evidence ↔ Event / entities
    "Means": Means,                # Object -> Event
    "EvidenceLink": EvidenceLink,  # Evidence -> (Event/Person/Location/Object/Statement)
}


# =========================
# EDGE TYPE MAPPING
# =========================
# Maps (source_entity_type, target_entity_type) -> [edge_type_names]
# This tells Graphiti which edge types are allowed between which node types.

edge_type_map = {
    # Person → Statement: who said / testified / denied what
    ("Person", "Statement"): ["StatementAttribution"],

    # Statement → Statement: conversational structure and logical relations
    ("Statement", "Statement"): ["StatementResponse", "StatementReference"],

    # Statement → other entities: references, descriptions, accusations, etc.
    ("Statement", "Person"): ["StatementReference"],
    ("Statement", "Event"): ["StatementReference"],
    ("Statement", "Location"): ["StatementReference"],
    ("Statement", "Object"): ["StatementReference"],
    ("Statement", "Organization"): ["StatementReference"],
    ("Statement", "Evidence"): ["StatementReference"],

    # Person → Event: classic detective concepts (motive, alibi, opportunity, suspicion, presence)
    ("Person", "Event"): ["Motive", "Alibi", "Opportunity", "Suspicion", "Presence"],

    # Person → Location: simple presence / visits (e.g., seen in corridor, garden, etc.)
    ("Person", "Location"): ["Presence"],

    # Object → Event: means (weapon, delivery method, tool)
    ("Object", "Event"): ["Means"],

    # Evidence → core entities: how evidence supports or contradicts them
    ("Evidence", "Event"): ["EvidenceLink"],
    ("Evidence", "Person"): ["EvidenceLink"],
    ("Evidence", "Location"): ["EvidenceLink"],
    ("Evidence", "Object"): ["EvidenceLink"],
    ("Evidence", "Statement"): ["EvidenceLink"],

    # Fallback: apply EvidenceLink generically when we still want a soft, schema-safe relation
    ("Entity", "Entity"): ["EvidenceLink"],
}
