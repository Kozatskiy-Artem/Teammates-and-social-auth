from dataclasses import dataclass


@dataclass(frozen=True)
class MemberDTO:
    id: int
    first_name: str
    last_name: str
    email: str


@dataclass(frozen=True)
class NewTeamDTO:
    name: str


@dataclass(frozen=True)
class TeamDTO:
    id: int
    name: str
    members: list[MemberDTO]


@dataclass(frozen=True)
class MemberIdDTO:
    id: int
