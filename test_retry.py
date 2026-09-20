from eventharvest.retry import with_retries


def test_retries_until_success(monkeypatch):
    calls = []

    def fake_sleep(_):
        pass

    monkeypatch.setattr("eventharvest.retry.time.sleep", fake_sleep)

    def operation():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("temporary")
        return "ok"

    assert with_retries(operation, attempts=3, base_delay=0, jitter=0) == "ok"
    assert len(calls) == 3
