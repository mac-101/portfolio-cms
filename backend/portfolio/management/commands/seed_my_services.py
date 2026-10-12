from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from portfolio.models import Portfolio, Service, SocialLink
from portfolio.utils import unique_portfolio_slug


SERVICES = [
    {
        "title": "Custom Websites",
        "summary": "Fast, mobile-first websites built from scratch to match your brand.",
        "features": [
            "Business websites",
            "Landing pages",
            "Portfolio sites",
            "Responsive on every device",
        ],
    },
    {
        "title": "Web Applications",
        "summary": "Full-stack apps with user accounts, a real database, and an admin dashboard to manage it all.",
        "features": [
            "User authentication",
            "Data management",
            "Admin dashboards",
            "Real-time features",
        ],
    },
    {
        "title": "APIs & Backend Development",
        "summary": "Secure REST APIs and database-backed backends that power your website or app.",
        "features": [
            "REST APIs with Django REST Framework",
            "PostgreSQL database design",
            "Authentication and permissions",
            "Deployment and image storage",
        ],
    },
]

SOCIAL_LINKS = [
    {
        "platform": "GitHub",
        "url": "https://github.com/mac-101",
        "label": "",
    },
    {
        "platform": "WhatsApp",
        "url": "https://wa.me/2349161489807?text=Hello%20Charles!%20I%27m%20interested%20in%20your%20web%20development%20services.%20Can%20we%20discuss%20my%20project%20requirements?",
        "label": "Get a free quote",
    },
]


class Command(BaseCommand):
    help = "Add MacAnthony's services and contact links to a user's portfolio."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="User who will own the services.")
        parser.add_argument(
            "--update", action="store_true",
            help="Overwrite services and links that already exist (default: leave them alone).",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            user = User.objects.get(username=options["username"])
        except User.DoesNotExist:
            raise CommandError(
                f'No user named "{options["username"]}". Sign up first, then run this again.'
            )

        portfolio, _ = Portfolio.objects.get_or_create(
            owner=user,
            defaults={"name": user.username, "slug": unique_portfolio_slug(user.username)},
        )

        # If the Service model gets a "features" field later, use it.
        # Until then, the feature list is added to the end of the description.
        has_features = any(f.name == "features" for f in Service._meta.get_fields())

        created = updated = skipped = 0

        # Service has no ordering field, so the API lists by id: create in the order above.
        for entry in SERVICES:
            if has_features:
                fields = {
                    "description": entry["summary"],
                    "features": "\n".join(entry["features"]),
                }
            else:
                fields = {
                    "description": f'{entry["summary"]} Includes: {", ".join(entry["features"])}.'
                }

            service, was_created = Service.objects.get_or_create(
                portfolio=portfolio, title=entry["title"], defaults=fields
            )
            if was_created:
                created += 1
            elif options["update"]:
                for key, value in fields.items():
                    setattr(service, key, value)
                service.save()
                updated += 1
            else:
                skipped += 1

        for entry in SOCIAL_LINKS:
            link, was_created = SocialLink.objects.get_or_create(
                portfolio=portfolio,
                platform=entry["platform"],
                defaults={"url": entry["url"], "label": entry["label"]},
            )
            if was_created:
                created += 1
            elif options["update"]:
                link.url, link.label = entry["url"], entry["label"]
                link.save()
                updated += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done for {user.username}: {created} created, {updated} updated, "
            f"{skipped} skipped (already exist)."
        ))