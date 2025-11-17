from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator


# =========================
# ENTITY TYPES
# =========================

class Person(BaseModel):
    """A person involved in a detective case (suspect, victim, witness, investigator, or other role)."""

    full_name: Optional[str] = Field(
        None,
        description="Full name of the person as mentioned in the case materials.",
    )
    alias: Optional[str] = Field(
        None,
        description="Alternative name, nickname, or title used for this person in the narrative.",
    )
    role_in_case: Optional[str] = Field(
        None,
        description="High-level role in the investigation (for example: suspect, victim, witness, inspector).",
    )
    age: Optional[int] = Field(
        None,
        description="Approximate age of the person at the time of the main events.",
    )
    occupation: Optional[str] = Field(
        None,
        description="Primary job or occupation as described in the story.",
    )
    primary_location: Optional[str] = Field(
        None,
        description="Main location associated with this person (for example: home or workplace).",
    )
    is_victim: Optional[bool] = Field(
        None,
        description="True if this person is explicitly described as a victim of a crime or attack.",
    )
    is_suspect: Optional[bool] = Field(
        None,
        description="True if this person is explicitly considered a suspect in the investigation.",
    )
    is_witness: Optional[bool] = Field(
        None,
        description="True if this person provides testimony or is described as having seen relevant events.",
    )


class Statement(BaseModel):
    """A spoken or written statement, quote, or testimony relevant to solving the case."""

    text: Optional[str] = Field(
        None,
        description="Exact or approximate content of the statement as it appears in the text.",
    )
    is_direct_quote: Optional[bool] = Field(
        None,
        description="True if the statement is presented as a direct quotation with quotation marks.",
    )
    is_under_oath: Optional[bool] = Field(
        None,
        description="True if the statement is given as formal testimony (for example, in court or to the police).",
    )
    source_document_id: Optional[str] = Field(
        None,
        description="Identifier of the source document or chapter where this statement appears, if available.",
    )
    paragraph_index: Optional[int] = Field(
        None,
        description="Zero-based index of the paragraph in which the statement appears, when known.",
    )


class Location(BaseModel):
    """A physical location referenced in the case, such as rooms, buildings, streets, or cities."""

    label: Optional[str] = Field(
        None,
        description="Short label for the location (for example: 'study', 'garden', 'opera house').",
    )
    address: Optional[str] = Field(
        None,
        description="Full or partial address of the location when provided in the text.",
    )
    building_name: Optional[str] = Field(
        None,
        description="Name of the building or estate, if applicable.",
    )
    room_name: Optional[str] = Field(
        None,
        description="Name or description of the specific room or interior area within a building.",
    )
    city: Optional[str] = Field(
        None,
        description="City or town in which this location is situated, if known.",
    )
    country: Optional[str] = Field(
        None,
        description="Country of the location, when specified.",
    )
    is_crime_scene: Optional[bool] = Field(
        None,
        description="True if this location is explicitly described as a scene of a crime, attack, or major event.",
    )


class Event(BaseModel):
    """An event relevant to the investigation, such as murders, robberies, meetings, or alibi intervals."""

    event_type: Optional[str] = Field(
        None,
        description="Short label describing the event type (for example: 'murder', 'robbery', 'alibi_interval').",
    )
    description: Optional[str] = Field(
        None,
        description="Narrative description of the event as inferred from the text.",
    )
    start_time: Optional[datetime] = Field(
        None,
        description="Approximate start time of the event when it can be inferred or is explicitly mentioned.",
    )
    end_time: Optional[datetime] = Field(
        None,
        description="Approximate end time of the event, if it spans a period of time.",
    )
    is_crime: Optional[bool] = Field(
        None,
        description="True if this event is itself a crime or attempted crime.",
    )
    is_confirmed: Optional[bool] = Field(
        None,
        description="True if the narrator treats the event as factual rather than hypothetical or speculative.",
    )


class Object(BaseModel):
    """A physical object relevant to the case, such as weapons, tools, documents, or personal items."""

    label: Optional[str] = Field(
        None,
        description="Short name or label for the object (for example: 'revolver', 'teacup', 'watch').",
    )
    category: Optional[str] = Field(
        None,
        description="Category of object (for example: 'weapon', 'document', 'clothing', 'tool').",
    )
    material: Optional[str] = Field(
        None,
        description="Primary material of the object (for example: 'metal', 'glass', 'paper').",
    )
    is_weapon: Optional[bool] = Field(
        None,
        description="True if the object is used or suspected to be used as a weapon.",
    )
    is_personal_item: Optional[bool] = Field(
        None,
        description="True if this object is personally associated with a specific character (for example: jewelry, watch).",
    )


class Evidence(BaseModel):
    """A piece of evidence collected or inferred in the investigation, physical or informational."""

    evidence_type: Optional[str] = Field(
        None,
        description="Type of evidence (for example: 'fingerprint', 'footprint', 'document', 'forensic_report').",
    )
    description: Optional[str] = Field(
        None,
        description="Short explanation of what this evidence is and why it matters.",
    )
    collected_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the evidence is collected, if explicitly known.",
    )
    collected_by: Optional[str] = Field(
        None,
        description="Name or role of the person who collected the evidence (for example: 'Holmes', 'inspector').",
    )
    chain_of_custody_id: Optional[str] = Field(
        None,
        description="Identifier tracking how this evidence moves between people or locations, if modeled.",
    )
    reliability_score: Optional[float] = Field(
        None,
        description="Normalized confidence score between 0.0 and 1.0 expressing how reliable this piece of evidence appears.",
    )

    @field_validator("reliability_score")
    @classmethod
    def validate_reliability_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("reliability_score must be between 0.0 and 1.0")
        return v


class Organization(BaseModel):
    """An organization appearing in the case, such as police forces, companies, or criminal groups."""

    org_name: Optional[str] = Field(
        None,
        description="Full name of the organization as mentioned in the story.",
    )
    org_type: Optional[str] = Field(
        None,
        description="Kind of organization (for example: 'police', 'bank', 'criminal_group', 'family').",
    )
    jurisdiction: Optional[str] = Field(
        None,
        description="Geographical or legal area in which the organization operates.",
    )
    industry: Optional[str] = Field(
        None,
        description="Main industry or activity of the organization where applicable (for example: 'finance', 'law enforcement').",
    )