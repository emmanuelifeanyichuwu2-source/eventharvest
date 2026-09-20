from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .models import Event, TicketOption

logger = logging.getLogger(__name__)


class EventExtractor:
    """Extract Event schema.org JSON-LD, with conservative HTML fallbacks."""

    def extract(self, html: str, *, url: str) -> list[Event]:
        soup = BeautifulSoup(html, "html.parser")
        events: list[Event] = []

        for payload in self._json_ld(soup):
            for item in self._flatten_json_ld(payload):
                if self._is_event(item):
                    event = self._from_schema(item, url=url)
                    if event:
                        events.append(event)

        if not events:
            fallback = self._fallback_event(soup, url=url)
            if fallback:
                events.append(fallback)

        return self._deduplicate(events)

    def _json_ld(self, soup: BeautifulSoup) -> Iterable[object]:
        for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
            try:
                yield json.loads(tag.string or tag.get_text())
            except json.JSONDecodeError:
                logger.warning("Ignoring malformed JSON-LD block")

    def _flatten_json_ld(self, payload: object) -> Iterable[dict]:
        if isinstance(payload, dict):
            yield payload
            graph = payload.get("@graph")
            if isinstance(graph, list):
                yield from self._flatten_json_ld(graph)
        elif isinstance(payload, list):
            for item in payload:
                yield from self._flatten_json_ld(item)

    @staticmethod
    def _is_event(item: dict) -> bool:
        kind = item.get("@type")
        if isinstance(kind, list):
            return "Event" in kind
        return kind == "Event"

    def _from_schema(self, item: dict, *, url: str) -> Event | None:
        name = self._text(item.get("name"))
        if not name:
            return None

        location = item.get("location") or {}
        if isinstance(location, list):
            location = location[0] if location else {}
        venue = self._text(location.get("name")) if isinstance(location, dict) else None

        tickets: list[TicketOption] = []
        offers = item.get("offers")
        for offer in offers if isinstance(offers, list) else [offers]:
            if not isinstance(offer, dict):
                continue
            price = self._number(offer.get("price"))
            tickets.append(
                TicketOption(
                    name=self._text(offer.get("name")) or "General admission",
                    price=price,
                    currency=self._text(offer.get("priceCurrency")),
                    availability=self._text(offer.get("availability")),
                )
            )

        return Event(
            name=name,
            url=urljoin(url, self._text(item.get("url")) or url),
            date=self._text(item.get("startDate")),
            venue=venue,
            description=self._text(item.get("description")),
            tickets=tickets,
            source=url,
        )

    def _fallback_event(self, soup: BeautifulSoup, *, url: str) -> Event | None:
        title = soup.select_one("[data-event-name], h1")
        if not title:
            return None
        name = title.get("data-event-name") or title.get_text(" ", strip=True)
        if not name:
            return None
        return Event(name=name, url=url, source=url)

    @staticmethod
    def _deduplicate(events: list[Event]) -> list[Event]:
        seen: set[tuple[str, str]] = set()
        unique: list[Event] = []
        for event in events:
            key = (event.name.casefold(), event.url)
            if key not in seen:
                seen.add(key)
                unique.append(event)
        return unique

    @staticmethod
    def _text(value: object) -> str | None:
        if value is None:
            return None
        if isinstance(value, dict):
            return str(value.get("name") or value.get("url") or "").strip() or None
        return str(value).strip() or None

    @staticmethod
    def _number(value: object) -> float | None:
        try:
            return float(value) if value is not None and str(value).strip() else None
        except (TypeError, ValueError):
            return None
