from dataclasses import dataclass
from base.DTO import IdMixinDTO, TimeMixinDTO


@dataclass
class UserShortInfo:
    username: str


@dataclass
class UserCreds(IdMixinDTO):
    password: str


@dataclass
class UserDTO(IdMixinDTO, TimeMixinDTO):
    username: str
    name: str | None
    is_active: bool
    is_verified: bool


@dataclass
class ProfileDTO(IdMixinDTO):
    bio: str | None
    age: str | None
    city: str | None

    user_id: int


@dataclass
class SettingsDTO(IdMixinDTO):
    show_in_search: bool
    is_profile_public: bool

    user_id: int


@dataclass
class UserProfileDTO:
    user: UserDTO
    profile: ProfileDTO



@dataclass
class UserSettingsDTO:
    user: UserDTO
    settings: SettingsDTO


@dataclass
class FullUserDTO:
    user: UserDTO
    profile: ProfileDTO
    settings: SettingsDTO

