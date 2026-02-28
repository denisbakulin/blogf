from dataclasses import dataclass
from datetime import datetime


@dataclass
class IdMixinDTO:
    id: int


@dataclass
class TimeMixinDTO:
    created_at: datetime


