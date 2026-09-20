from pathlib import Path

from eventharvest.extractor import EventExtractor


HTML = Path(__file__).parent.joinpath("fixtures/event.html").read_text(encoding="utf-8")


def test_extracts_schema_event_and_offers():
    events = EventExtractor().extract(HTML, url="https://example.test/events/1")

    assert len(events) == 1
    event = events[0]
    assert event.name == "Open Data Night"
    assert event.venue == "Civic Hall"
    assert event.url == "https://example.test/events/open-data-night"
    assert [ticket.price for ticket in event.tickets] == [25.0, 10.0]


def test_falls_back_to_h1_when_schema_is_absent():
    html = "<html><body><h1>Fallback Event</h1></body></html>"
    events = EventExtractor().extract(html, url="https://example.test/fallback")

    assert len(events) == 1
    assert events[0].name == "Fallback Event"
