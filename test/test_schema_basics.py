import json
from jsonschema import validate

from backend.app.scraper.parser import parse_document


def minimal_html():
    return """
    <html lang="en">
      <head>
        <title>Test Page</title>
        <meta name="description" content="Test description" />
      </head>
      <body>
        <header><h1>Hero Title</h1></header>
        <main>
          <section>
            <h2>Section One</h2>
            <p>Hello world.</p>
            <a href="/about">About</a>
          </section>
        </main>
        <footer>Footer content</footer>
      </body>
    </html>
    """


RESULT_SCHEMA = {
    "type": "object",
    "required": ["url", "scrapedAt", "meta", "sections"],
    "properties": {
      "url": {"type": "string"},
      "scrapedAt": {"type": "string"},
      "meta": {
        "type": "object",
        "required": ["title", "description", "language", "canonical"],
      },
      "sections": {
        "type": "array",
        "items": {
          "type": "object",
          "required": [
            "id",
            "type",
            "label",
            "sourceUrl",
            "content",
            "rawHtml",
            "truncated"
          ]
        }
      }
    }
}


def test_parse_document_schema_minimal():
    html = minimal_html()
    result = parse_document(
        input_url="https://example.com",
        html=html,
        base_url="https://example.com",
        strategy="static",
    )

    validate(instance=result, schema=RESULT_SCHEMA)

    assert result["url"] == "https://example.com"
    assert len(result["sections"]) >= 1
    texts = [s["content"]["text"] for s in result["sections"]]
    assert any("Hello world" in t for t in texts)
