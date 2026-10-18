from pathlib import Path

import markdown
from django.conf import settings

DOCS_DIR = Path(settings.BASE_DIR) / "docs_content"

# (slug, title). The slug is also the file name: docs_content/<slug>.md
DOC_SECTIONS = [
    ("Start here", [
        ("introduction", "Introduction"),
        ("quick-start", "Quick start"),
        ("api-basics", "API basics"),
    ]),
    ("Endpoints", [
        ("projects", "Projects"),
        ("tech-stack", "Tech stack"),
        ("services", "Services"),
        ("social-links", "Social links"),
        ("portfolio", "Portfolio"),
    ]),
    ("Guides", [
        ("html-guide", "Plain HTML and JavaScript"),
        ("react-guide", "React"),
        ("icons", "Using icons"),
        ("deploying", "Deploying your frontend"),
    ]),
    ("More", [
        ("faq", "FAQ and troubleshooting"),
        ("changelog", "Changelog"),
        ("credits", "Credits"),
    ]),
]

PAGES = [page for _, pages in DOC_SECTIONS for page in pages]
TITLES = dict(PAGES)
ORDER = [slug for slug, _ in PAGES]


def render_page(slug):
    """Return the page as HTML, or None. Only slugs in the list above can be opened."""
    if slug not in TITLES:
        return None
    path = DOCS_DIR / f"{slug}.md"
    if not path.is_file():
        return None

    text = path.read_text(encoding="utf-8")
    text = text.replace("{{ product_name }}", settings.PRODUCT_NAME)
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    return md.convert(text)