import json
from pathlib import Path
from bs4 import BeautifulSoup

html = Path("event.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

events = []
for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
    payload = json.loads(tag.string or tag.get_text())
    if payload.get("@type") == "Event":
        events.append({
            "name": payload.get("name"),
            "url": "https://example.test" + payload.get("url", ""),
            "date": payload.get("startDate"),
            "venue": (payload.get("location") or {}).get("name"),
            "description": payload.get("description"),
            "tickets": [
                {
                    "name": offer.get("name", "General admission"),
                    "price": float(offer["price"]) if offer.get("price") else None,
                    "currency": offer.get("priceCurrency"),
                    "availability": offer.get("availability"),
                }
                for offer in payload.get("offers", [])
            ],
            "source": "https://example.test/events/1",
        })

print(json.dumps(events, indent=2))
