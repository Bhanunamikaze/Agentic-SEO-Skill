import json
from pathlib import Path

import pagespeed


FIXTURES = Path(__file__).parent / "fixtures"


class DummyResponse:
    def __init__(self, status_code, payload=None, json_error=None):
        self.status_code = status_code
        self.payload = payload or {}
        self.json_error = json_error

    def json(self):
        if self.json_error:
            raise self.json_error
        return self.payload


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_parse_pagespeed_response_uses_field_data_when_available():
    result = pagespeed.parse_pagespeed_response(
        load_fixture("pagespeed_field_data.json"),
        url="https://example.com/",
        strategy="mobile",
    )

    assert result["error"] is None
    assert result["performance_score"] == 92
    assert result["field_data_available"] is True
    assert result["metrics"]["LCP"]["value"] == 1800
    assert result["metrics"]["INP"]["rating"] == "fast"
    # PSI reports CLS as an integer scaled by 100; the parser rescales it so the
    # value matches CWV_THRESHOLDS and the lab fallback.
    assert result["metrics"]["CLS"]["value"] == 0.06
    assert result["opportunities"][0]["title"] == "Reduce unused JavaScript"
    assert result["diagnostics"][0]["title"] == "Avoid an excessive DOM size"


def test_parse_pagespeed_response_falls_back_to_lab_data():
    result = pagespeed.parse_pagespeed_response(
        load_fixture("pagespeed_lab_data.json"),
        url="https://example.com/",
        strategy="desktop",
    )

    assert result["performance_score"] == 57
    assert result["field_data_available"] is False
    assert result["metrics"]["LCP"]["rating"] == "poor"
    assert result["metrics"]["CLS"]["value"] == 0.12
    assert result["metrics"]["TTFB"]["rating"] == "good"


def test_get_pagespeed_retries_rate_limit_and_then_parses(monkeypatch):
    responses = [
        DummyResponse(429),
        DummyResponse(200, load_fixture("pagespeed_field_data.json")),
    ]
    sleeps = []

    def fake_get(*args, **kwargs):
        return responses.pop(0)

    monkeypatch.setattr(pagespeed, "safe_get", fake_get)
    monkeypatch.setattr(pagespeed.time, "sleep", lambda seconds: sleeps.append(seconds))

    result = pagespeed.get_pagespeed("https://example.com/", strategy="mobile")

    assert result["error"] is None
    assert result["performance_score"] == 92
    assert sleeps == [3]


def test_get_pagespeed_reports_invalid_json(monkeypatch):
    monkeypatch.setattr(pagespeed, "safe_get", lambda *args, **kwargs: DummyResponse(200, json_error=ValueError("bad json")))

    result = pagespeed.get_pagespeed("https://example.com/", strategy="mobile")

    assert result["performance_score"] is None
    assert "Failed to parse API response" in result["error"]


def test_get_pagespeed_for_strategies_keeps_each_strategy(monkeypatch):
    def fake_get_pagespeed(url, strategy="mobile", api_key=None):
        return {"url": url, "strategy": strategy, "performance_score": 90 if strategy == "mobile" else 70, "error": None}

    monkeypatch.setattr(pagespeed, "get_pagespeed", fake_get_pagespeed)

    result = pagespeed.get_pagespeed_for_strategies("https://example.com/", ["mobile", "desktop"])

    assert result["error"] is None
    assert result["strategies"]["mobile"]["performance_score"] == 90
    assert result["strategies"]["desktop"]["performance_score"] == 70
