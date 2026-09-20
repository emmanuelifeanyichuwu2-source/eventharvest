from __future__ import annotations

import time


class RateLimiter:
    """Simple process-local minimum-interval rate limiter."""

    def __init__(self, requests_per_second: float = 1.0) -> None:
        if requests_per_second <= 0:
            raise ValueError("requests_per_second must be greater than zero")
        self.interval = 1.0 / requests_per_second
        self._last_request = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        remaining = self.interval - (now - self._last_request)
        if remaining > 0:
            time.sleep(remaining)
        self._last_request = time.monotonic()
