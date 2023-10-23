from dataclasses import dataclass


@dataclass(frozen=True)
class OAuthDTO:
    code: str


@dataclass(frozen=True)
class OAuthResponseDTO:
    email: str
    first_name: str
    last_name: str


@dataclass(frozen=True)
class OAuthLoginResponseDTO:
    access_token: str
    refresh_token: str
