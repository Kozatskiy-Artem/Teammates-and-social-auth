from dataclasses import dataclass


@dataclass(frozen=True)
class NewTeamDTO:
    name: str


@dataclass(frozen=True)
class TeamDTO:
    id: int
    name: str
