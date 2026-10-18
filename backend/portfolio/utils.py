from django.utils.text import slugify

from .models import Portfolio

RESERVED = {"admin", "api", "dashboard", "login", "logout", "signup", "static", "media", "docs", "feedback"}

def unique_portfolio_slug(base):
    base = slugify(base)[:40] or "portfolio"
    if base in RESERVED:
        base = f"{base}-dev"
    slug, n = base, 2
    while slug in RESERVED or Portfolio.objects.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug