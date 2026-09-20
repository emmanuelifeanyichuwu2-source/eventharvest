from eventharvest.rate_limit import RateLimiter


def test_rejects_invalid_rate():
    try:
        RateLimiter(0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
