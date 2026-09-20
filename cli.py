from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from .pipeline import Pipeline
from .rate_limit import RateLimiter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract structured event data from public web pages.")
    parser.add_argument("urls", nargs="+", help="Public event page URLs")
    parser.add_argument("--output", type=Path, help="Write JSON output to this file")
    parser.add_argument("--rps", type=float, default=1.0, help="Maximum requests per second")
    parser.add_argument("--attempts", type=int, default=3, help="HTTP retry attempts")
    parser.add_argument("--verbose", action="store_true", help="Enable INFO logging")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING, format="%(levelname)s %(message)s")
    pipeline = Pipeline()
    pipeline.client.limiter = RateLimiter(args.rps)
    pipeline.client.attempts = args.attempts

    data = [event.to_dict() for event in pipeline.run(args.urls)]
    rendered = json.dumps(data, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
