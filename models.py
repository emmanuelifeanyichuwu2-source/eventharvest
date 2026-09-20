from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class TicketOption:
    name: str
    price: float | None = None
    currency: str | None = None
    availability: str | None = None


@dataclass(slots=True)
class Event:
    name: str
    url: str
    date: str | None = None
    venue: str | None = None
    description: str | None = None
    tickets: list[TicketOption] = field(default_factory=list)
    source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
