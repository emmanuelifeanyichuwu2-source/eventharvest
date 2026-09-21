# EventHarvest Demo

This is a self-contained demonstration of EventHarvest's structured event extraction workflow.

## What it demonstrates

- Detecting Schema.org `Event` JSON-LD
- Extracting event name, date, venue, and description
- Extracting ticket price, currency, and availability
- Producing normalized JSON output

## Demo result

The included `demo_output.json` is the deterministic output produced from `event.html`.

**Event:** Open Data Night  
**Venue:** Civic Hall  
**Date:** 2026-10-15 18:00 +01:00  
**Standard ticket:** USD 25  
**Student ticket:** USD 10

## Running the demo

The demo uses only the included local fixture, so it does not depend on a third-party website.

```bash
python demo.py
```

The full EventHarvest source repository additionally demonstrates retries, rate limiting, logging, HTTP error handling, CLI usage, and automated tests.
