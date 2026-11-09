import javascript_render_audit as jra


class DummyResponse:
    def __init__(self, status_code, payload=None, headers=None):
        self.status_code = status_code
        self.payload = payload or {}
        self.headers = headers or {}

    def json(self):
        return self.payload


def fail_post(*args, **kwargs):
    raise AssertionError("Firecrawl must not be called")


def test_auto_without_key_keeps_playwright_result(monkeypatch):
    monkeypatch.setattr(jra, "get_env", lambda *names, default="": "")
    monkeypatch.setattr(jra, "render_with_playwright", lambda url, timeout_ms: (None, "playwright not installed"))
    monkeypatch.setattr(jra, "safe_post", fail_post)

    assert jra.render_page("https://example.com/", 30000) == (None, "playwright not installed", None)


def test_auto_with_key_only_hints_at_firecrawl(monkeypatch):
    monkeypatch.setattr(jra, "get_env", lambda *names, default="": "fc-test")
    monkeypatch.setattr(jra, "render_with_playwright", lambda url, timeout_ms: (None, "playwright not installed"))
    monkeypatch.setattr(jra, "safe_post", fail_post)

    html, error, renderer = jra.render_page("https://example.com/", 30000)

    assert html is None and renderer is None
    assert error == "playwright not installed; pass --renderer firecrawl to render with Firecrawl"


def test_firecrawl_renderer_retries_with_retry_after(monkeypatch):
    calls = []
    sleeps = []
    responses = [
        DummyResponse(429, {"error": "Rate limit exceeded"}, {"Retry-After": "5"}),
        DummyResponse(200, {"success": True, "data": {"rawHtml": "<html><h1>Rendered</h1></html>"}}),
    ]

    def fake_post(url, **kwargs):
        calls.append(kwargs)
        return responses.pop(0)

    monkeypatch.setattr(jra, "get_env", lambda *names, default="": "fc-test")
    monkeypatch.setattr(jra, "assert_safe_url", lambda url: url)
    monkeypatch.setattr(jra, "safe_post", fake_post)
    monkeypatch.setattr(jra.time, "sleep", lambda seconds: sleeps.append(seconds))

    html, error, renderer = jra.render_page("https://example.com/", 30000, renderer="firecrawl")

    assert (html, error, renderer) == ("<html><h1>Rendered</h1></html>", None, "firecrawl")
    assert sleeps == [5.0]
    assert calls[0]["json"]["formats"] == ["rawHtml"]
    assert calls[0]["json"]["origin"] == "agentic-seo-skill"
    assert calls[0]["allow_redirects"] is False


def test_firecrawl_auth_error_is_reported_without_retry(monkeypatch):
    calls = []

    def fake_post(url, **kwargs):
        calls.append(url)
        return DummyResponse(401, {"success": False, "error": "Unauthorized: Invalid token"})

    monkeypatch.setattr(jra, "get_env", lambda *names, default="": "fc-bad")
    monkeypatch.setattr(jra, "assert_safe_url", lambda url: url)
    monkeypatch.setattr(jra, "safe_post", fake_post)

    html, error, renderer = jra.render_page("https://example.com/", 30000, renderer="firecrawl")

    assert html is None and renderer is None
    assert error == "firecrawl HTTP 401: Unauthorized: Invalid token"
    assert len(calls) == 1


def test_firecrawl_renderer_without_key(monkeypatch):
    monkeypatch.setattr(jra, "get_env", lambda *names, default="": "")
    monkeypatch.setattr(jra, "safe_post", fail_post)

    assert jra.render_page("https://example.com/", 30000, renderer="firecrawl") == (
        None,
        "FIRECRAWL_API_KEY not set",
        None,
    )


def test_firecrawl_renderer_refuses_private_ip(monkeypatch):
    monkeypatch.setattr(jra, "get_env", lambda *names, default="": "fc-test")
    monkeypatch.setattr(jra, "safe_post", fail_post)

    html, error, renderer = jra.render_page("http://10.0.0.5/admin", 30000, renderer="firecrawl")

    assert html is None and renderer is None
    assert error.startswith("not sent to firecrawl: Blocked")
