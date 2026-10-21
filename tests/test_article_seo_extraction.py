import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location("article_seo", SCRIPTS / "article_seo.py")
article_seo = importlib.util.module_from_spec(spec)
sys.modules["article_seo"] = article_seo
spec.loader.exec_module(article_seo)

from bs4 import BeautifulSoup  # noqa: E402


# No class~=author, no span[itemprop=author], no a[rel=author]. Author and date are
# carried only by meta tags, <time> and JSON-LD — the shape a Next.js/Astro site emits.
META_ONLY = """<!doctype html>
<html lang="en">
<head>
  <title>Procedural puzzle generation</title>
  <meta name="author" content="Ada Analyst">
  <meta property="article:published_time" content="2026-08-10T00:00:00.000Z">
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"BlogPosting",
   "author":{"@type":"Person","name":"Ada Analyst"},
   "datePublished":"2026-08-10T00:00:00.000Z"}
  </script>
</head>
<body><main><h1>Procedural puzzle generation</h1><p>Body copy.</p></main></body>
</html>"""

# Author and date reachable only through JSON-LD, and nested under @graph.
JSONLD_GRAPH_ONLY = """<!doctype html>
<html lang="en">
<head>
  <title>Graph only</title>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[
    {"@type":"WebSite","name":"Example"},
    {"@type":"BlogPosting","author":{"@type":"Person","name":"Grace Graph"},
     "datePublished":"2026-07-01"}
  ]}
  </script>
</head>
<body><main><h1>Graph only</h1><p>Body copy.</p></main></body>
</html>"""

TIME_ELEMENT_ONLY = """<!doctype html>
<html lang="en">
<head><title>Time only</title></head>
<body><main><h1>Time only</h1><time datetime="2026-06-15">15 June 2026</time></main></body>
</html>"""


def _extract(html):
    soup = BeautifulSoup(html, "html.parser")
    return article_seo.extract_content(soup, article_seo.detect_cms(soup, ""))


def test_author_from_meta_tag():
    assert _extract(META_ONLY)["author"] == "Ada Analyst"


def test_publish_date_from_opengraph_property_attribute():
    # Regression: the selector used {"name": "article:published_time"}, but OpenGraph
    # emits property=, so this returned "" on every standards-compliant page.
    assert _extract(META_ONLY)["publish_date"].startswith("2026-08-10")


def test_author_and_date_from_jsonld_graph():
    result = _extract(JSONLD_GRAPH_ONLY)
    assert result["author"] == "Grace Graph"
    assert result["publish_date"].startswith("2026-07-01")


def test_publish_date_from_time_element():
    assert _extract(TIME_ELEMENT_ONLY)["publish_date"].startswith("2026-06-15")


def test_visible_byline_still_wins_over_jsonld_absence():
    html = """<html><head><title>T</title></head><body><main>
    <p class="byline">By Classic Byline</p><h1>T</h1></main></body></html>"""
    assert _extract(html)["author"] == "By Classic Byline"
