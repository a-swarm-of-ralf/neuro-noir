from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator

# =========================
# RELATION / EDGE TYPES
# =========================

class StatementAttribution(BaseModel):
    """Relationship assigning a statement to the person who produced it, including the speech act type."""

    speech_act_type: Optional[
        Literal["said", "testified", "denied"]
    ] = Field(
        None,
        description=(
            "Type of speech act linking the person to the statement. "
            "Use 'said' for informal quotes, 'testified' for formal testimony, "
            "and 'denied' when the statement explicitly rejects a claim."
        ),
    )
    is_explicit: Optional[bool] = Field(
        None,
        description="True if the text explicitly attributes the statement to the person, false if it is inferred.",
    )
    confidence_score: Optional[float] = Field(
        None,
        description="Normalized confidence between 0.0 and 1.0 that this attribution is correct.",
    )
    source_reference: Optional[str] = Field(
        None,
        description="Optional reference to the passage or document that supports this attribution.",
    )

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("confidence_score must be between 0.0 and 1.0")
        return v


class StatementResponse(BaseModel):
    """Relationship indicating that one statement responds to or follows from another statement."""

    response_type: Optional[
        Literal["responded_to", "follow_up", "agreement", "disagreement"]
    ] = Field(
        None,
        description=(
            "Specific response subtype connecting the two statements. "
            "Use 'responded_to' for direct answers, 'follow_up' for continuation, "
            "'agreement' or 'disagreement' when explicitly indicated."
        ),
    )
    is_direct: Optional[bool] = Field(
        None,
        description="True if the response is immediate and clearly linked in the dialogue.",
    )
    justification: Optional[str] = Field(
        None,
        description="Short natural language explanation of how the text indicates this response relationship.",
    )


class StatementReference(BaseModel):
    """Relationship where a statement refers to, describes, or accuses another entity or event."""

    reference_type: Optional[
        Literal["refers_to", "describes", "accuses", "supports", "contradicts"]
    ] = Field(
        None,
        description=(
            "Role of the target in relation to the statement. "
            "Use 'refers_to' for mentions, 'describes' for descriptive passages, "
            "'accuses' when blaming a person, 'supports' or 'contradicts' for evidential relationships."
        ),
    )
    salience_score: Optional[float] = Field(
        None,
        description="Normalized score between 0.0 and 1.0 representing how central this target is to the statement.",
    )
    explanation: Optional[str] = Field(
        None,
        description="Short explanation of why the statement is linked to this target in this way.",
    )

    @field_validator("salience_score")
    @classmethod
    def validate_salience_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("salience_score must be between 0.0 and 1.0")
        return v


class Motive(BaseModel):
    """Motive relationship connecting a person to an event they have a reason to cause."""

    motive_type: Optional[str] = Field(
        None,
        description="Type of motive (for example: 'financial', 'revenge', 'jealousy', 'self_preservation').",
    )
    strength_score: Optional[float] = Field(
        None,
        description="Normalized score between 0.0 and 1.0 indicating how strong the motive appears in the text.",
    )
    supporting_statement_id: Optional[str] = Field(
        None,
        description="Identifier of a key statement that expresses or reveals this motive, when available.",
    )
    explanation: Optional[str] = Field(
        None,
        description="Short explanation of why this person is considered to have a motive for this event.",
    )

    @field_validator("strength_score")
    @classmethod
    def validate_strength_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("strength_score must be between 0.0 and 1.0")
        return v


class Alibi(BaseModel):
    """Alibi relationship describing a person's claimed or verified absence from an event."""

    location_description: Optional[str] = Field(
        None,
        description="Text description of where the person claims to have been during the relevant event.",
    )
    start_time: Optional[str] = Field(
        None,
        description="Start of the time interval covered by the alibi, when it can be inferred.",
    )
    end_time: Optional[str] = Field(
        None,
        description="End of the time interval covered by the alibi, when it can be inferred.",
    )
    is_verified: Optional[bool] = Field(
        None,
        description="True if the alibi is supported by independent evidence in the narrative.",
    )
    verification_source: Optional[str] = Field(
        None,
        description="Short description of the source that verifies or falsifies this alibi (for example: 'ticket stub', 'witness testimony').",
    )


class Means(BaseModel):
    """Means relationship linking an object to an event where it is used as a tool, weapon, or mechanism."""

    means_role: Optional[str] = Field(
        None,
        description="Short label describing the role of the object in the event (for example: 'weapon', 'delivery_method').",
    )
    lethality_score: Optional[float] = Field(
        None,
        description="Normalized score between 0.0 and 1.0 indicating how dangerous or decisive the means appears.",
    )
    explanation: Optional[str] = Field(
        None,
        description="Short explanation of how the object functions as a means in the event.",
    )

    @field_validator("lethality_score")
    @classmethod
    def validate_lethality_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("lethality_score must be between 0.0 and 1.0")
        return v


class Opportunity(BaseModel):
    """Opportunity relationship connecting a person to an event they could realistically have carried out."""

    window_start: Optional[str] = Field(
        None,
        description="Earliest plausible time at which the person could have acted in relation to the event.",
    )
    window_end: Optional[str] = Field(
        None,
        description="Latest plausible time at which the person could have acted in relation to the event.",
    )
    is_unique: Optional[bool] = Field(
        None,
        description="True if the narrative suggests few or no other people had a similar opportunity.",
    )
    explanation: Optional[str] = Field(
        None,
        description="Short explanation of how the person's location and timing create an opportunity for this event.",
    )


class Presence(BaseModel):
    """Presence relationship linking a person to a location or event where they are described as being present."""

    presence_type: Optional[
        Literal["present_at", "visited"]
    ] = Field(
        None,
        description=(
            "Subtype of presence. Use 'present_at' for being at a location or event during critical moments, "
            "and 'visited' for more general or earlier visits."
        ),
    )
    arrival_time: Optional[str] = Field(
        None,
        description="Approximate time the person arrived at the location or event.",
    )
    departure_time: Optional[str] = Field(
        None,
        description="Approximate time the person left the location or event.",
    )
    is_confirmed: Optional[bool] = Field(
        None,
        description="True if the presence is confirmed by narration or multiple sources rather than speculation.",
    )
    explanation: Optional[str] = Field(
        None,
        description="Short explanation describing the evidence for this presence relationship.",
    )


class Suspicion(BaseModel):
    """Suspicion relationship linking a person to an event they are suspected of causing or participating in."""

    suspicion_level: Optional[float] = Field(
        None,
        description="Normalized score between 0.0 and 1.0 indicating the intensity of suspicion in the narrative.",
    )
    is_official: Optional[bool] = Field(
        None,
        description="True if suspicion is held by official investigators rather than only by private characters.",
    )
    explanation: Optional[str] = Field(
        None,
        description="Short explanation of why this person is suspected in relation to this event.",
    )

    @field_validator("suspicion_level")
    @classmethod
    def validate_suspicion_level(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("suspicion_level must be between 0.0 and 1.0")
        return v


class EvidenceLink(BaseModel):
    """General evidence relationship linking a piece of evidence to a person, event, location, or object."""

    link_type: Optional[
        Literal["evidence_of", "supports", "contradicts"]
    ] = Field(
        None,
        description=(
            "Type of evidential link. Use 'evidence_of' for direct linkage, 'supports' for corroborating evidence, "
            "and 'contradicts' for evidence that undermines a claim or alibi."
        ),
    )
    reliability_score: Optional[float] = Field(
        None,
        description="Normalized confidence between 0.0 and 1.0 that this evidence correctly relates to the target.",
    )
    explanation: Optional[str] = Field(
        None,
        description="Short explanation describing how the evidence connects to the target entity or event.",
    )

    @field_validator("reliability_score")
    @classmethod
    def validate_evidence_reliability_score(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("reliability_score must be between 0.0 and 1.0")
        return v
