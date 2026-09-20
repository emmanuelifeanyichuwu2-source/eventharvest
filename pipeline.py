from __future__ import annotations

import logging
from collections.abc import Iterable

from .client import FetchError, HttpClient
from .extractor import EventExtractor
from .models import Event

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, client: HttpClient | None = None, extractor: EventExtractor | None = None) -> None:
        self.client = client or HttpClient()
        self.extractor = extractor or EventExtractor()

    def run(self, urls: Iterable[str]) -> list[Event]:
        events: list[Event] = []
        for url in urls:
            try:
                html = self.client.get(url)
                extracted = self.extractor.extract(html, url=url)
                logger.info("Extracted %d event(s) from %s", len(extracted), url)
                events.extend(extracted)
            except FetchError as exc:
                logger.error("Skipping %s: %s", url, exc)
        return events
