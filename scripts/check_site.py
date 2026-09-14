"""Smoke-test the built one-page site: python3 scripts/check_site.py [output-dir]."""

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


BRAND = "impact works"
VISION = "The best technology in the hands of people doing good in the world."
MISSION = (
    "Rooted in our community, we partner with small mission-driven organizations "
    "to build and share excellent technology that multiplies their impact."
)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.body_text = []
        self.in_body = False
        self.heading_level = None
        self.headings = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "body":
            self.in_body = True
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_level = tag
            self.headings.append([tag, []])

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
        if tag == self.heading_level:
            self.heading_level = None

    def handle_data(self, data):
        if self.in_body:
            self.body_text.append(data)
        if self.heading_level:
            self.headings[-1][1].append(data)

    def elements(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


def normalize(parts):
    return " ".join(" ".join(parts).split())


root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
index = root / "index.html"
assert index.is_file(), "Missing built homepage"
assert sorted(root.rglob("*.html")) == [index], "The site must contain only the homepage"

page = Page(index)
assert len(page.elements("main")) == 1, "Expected one main landmark"
assert len(page.elements("h1")) == 1, "Expected one H1"
assert page.headings == [["h1", [BRAND]]], f"Unexpected headings: {page.headings}"
assert normalize(page.body_text) == f"{BRAND} {VISION} {MISSION}", "Unexpected visible copy"
assert not any(page.elements(tag) for tag in ["script", "form", "img", "nav", "header", "footer"])
assert len(page.elements("link")) == 2, "Expected canonical and local stylesheet links"

for attrs in page.elements("link"):
    href = attrs.get("href", "")
    if attrs.get("rel") != "stylesheet":
        continue
    url = urlsplit(href)
    assert not url.scheme and not url.netloc, "Stylesheet must be local"
    target = root / unquote(url.path).lstrip("/")
    assert target.is_file(), f"Missing stylesheet: {href}"

print("Passed: one page, exact approved copy, semantic structure, and local assets.")
