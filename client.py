from __future__ import annotations

import logging

import requests

from .rate_limit import RateLimiter
from .retry import with_retries

logger = logging.getLogger(__name__)


class FetchError(RuntimeError):
    """Raised when a page cannot be fetched successfully."""


class HttpClient:
    def __init__(
        self,
        *,
        requests_per_second: float = 1.0,
        timeout: float = 15.0,
        attempts: int = 3,
        user_agent: str = "EventHarvest/0.1 (+https://github.com/example/eventharvest)",
    ) -> None:
        self.timeout = timeout
        self.attempts = attempts
        self.limiter = RateLimiter(requests_per_second)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def get(self, url: str) -> str:
        def fetch() -> str:
            self.limiter.wait()
            logger.info("GET %s", url)
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text

        try:
            return with_retries(
                fetch,
                attempts=self.attempts,
                retry_on=(requests.RequestException,),
            )
        except requests.RequestException as exc:
            raise FetchError(f"Could not fetch {url}: {exc}") from exc
