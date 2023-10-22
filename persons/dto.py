from dataclasses import dataclass

from teams.dto import TeamDTO


@dataclass(frozen=True)
class NewPersonDTO:
    first_name: str
    last_name: str
    email: str


@dataclass(frozen=True)
class PersonDTO:
    id: int
    first_name: str
    last_name: str
    email: str
    team: TeamDTO
