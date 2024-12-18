from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import  Optional


@dataclass
class MatchEvent:
    type: str
    player: Optional[str] = None
    team: Optional[str] = None
    minute: Optional[int] = None
    pass_recipient: Optional[str] = None


class MatchNarrativeRequest(BaseModel):
    match_id: int = Field(..., description="ID da partida")
    style: str = Field(
        ...,
        description="Estilo da narração (formal, humoristico, tecnico)",
        pattern="^(formal|humoristico|tecnico)$",
    )


@dataclass
class MatchNarrativeResponse:
    narrative: str


class PlayerProfileRequest(BaseModel):
    match_id: int = Field(..., description="ID da partida")
    player_name: str = Field(..., description="Nome do jogador")


@dataclass
class PlayerStatistics:
    passes: int
    shots: int
    tackles: int
    minutes_played: int


@dataclass
class PlayerProfileResponse:
    name: str
    match_id: int
    statistics: PlayerStatistics
    team: str
    player_id: int
    player_position: list



class MatchSummaryRequest(BaseModel):
    match_id: int = Field(..., description="ID da partida")


@dataclass
class MatchSummaryResponse:
    match_summary: str