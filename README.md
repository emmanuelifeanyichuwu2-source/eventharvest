# EventHarvest

A small, open-source pipeline for extracting structured event information from public web pages.

EventHarvest is designed as a portfolio-quality example of resilient web data extraction. It focuses on predictable extraction, respectful request pacing, retry handling, validation-friendly models, logging, and machine-readable JSON output.

## Features

- Extracts Schema.org `Event` JSON-LD from HTML pages
- Handles JSON-LD arrays and `@graph` payloads
- Extracts event name, date, venue, description, ticket price, currency, and availability
- Conservative HTML fallback when structured data is unavailable
- Exponential-backoff retries with jitter
- Configurable request rate limiting
- Request timeout and HTTP error handling
- Structured Python dataclasses and JSON serialization
- CLI for batch processing of public URLs
- Automated tests and a local HTML fixture

## Responsible use

Only fetch pages you are allowed to access. Respect a site's terms, robots guidance, authentication boundaries, and published rate limits. EventHarvest deliberately does **not** attempt to defeat CAPTCHAs, authentication, paywalls, or other access controls. When a site presents an anti-bot challenge, the appropriate behavior for an automated pipeline is to stop, record the failure, and use an authorized/manual workflow if one exists.

## Quick start

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -e ".[test]"
pytest
```

Run against a public page you are permitted to fetch:

```bash
eventharvest https://example.com/events/example --output output.json --verbose
```

Or:

```bash
python -m eventharvest.cli https://example.com/events/example
```

## Example output

```json
[
  {
    "name": "Open Data Night",
    "url": "https://example.test/events/open-data-night",
    "date": "2026-10-15T18:00:00+01:00",
    "venue": "Civic Hall",
    "description": "A demo event used for EventHarvest tests.",
    "tickets": [
      {
        "name": "Standard",
        "price": 25.0,
        "currency": "USD",
        "availability": "https://schema.org/InStock"
      }
    ],
    "source": "https://example.test/events/1"
  }
]
```

## Project structure

```text
src/eventharvest/
├── client.py       # HTTP, timeout, retry integration
├── extractor.py    # JSON-LD and HTML extraction
├── models.py       # Output data models
├── pipeline.py     # Multi-URL orchestration
├── rate_limit.py   # Request pacing
├── retry.py        # Exponential backoff
└── cli.py          # Command-line interface

tests/
├── fixtures/
└── test_*.py
```

## Roadmap

- Pluggable site-specific extractors
- Persistent job state for scheduled runs
- Export adapters for CSV/JSONL
- Metrics and richer structured logging
- Optional proxy configuration for environments where proxy use is authorized
