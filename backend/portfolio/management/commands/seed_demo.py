from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from portfolio.models import Portfolio, Project, Service, SocialLink, TechStack

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo users and portfolio data for development."

    def handle(self, *args, **options):
        self._make("macanthony", "MacAnthony", [
            ("EchoNote", "A Django notes application.", True, True, ["Python", "Django"]),
            ("KFARM", "A website for a fish farming business.", True, True, ["React", "Tailwind CSS"]),
            ("Draft Project", "Not published yet.", False, False, ["Python"]),
        ])
        self._make("john", "John", [
            ("John's Store", "An online store.", False, True, ["React"]),
            ("John's Blog", "A personal blog.", False, True, ["Django"]),
        ])
        self.stdout.write(self.style.SUCCESS("Demo data ready."))

    def _make(self, username, name, projects):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password("demo12345")  # development only
            user.save()

        portfolio, _ = Portfolio.objects.get_or_create(
            owner=user, defaults={"name": name, "slug": username}
        )

        tech = {}
        for tech_name in ["Python", "Django", "React", "Tailwind CSS", "PostgreSQL"]:
            tech[tech_name], _ = TechStack.objects.get_or_create(
                portfolio=portfolio, name=tech_name
            )

        for title, desc, featured, published, techs in projects:
            project, _ = Project.objects.get_or_create(
                portfolio=portfolio,
                title=title,
                defaults={"description": desc, "featured": featured, "published": published},
            )
            project.tech_stack.set([tech[t] for t in techs])

        Service.objects.get_or_create(portfolio=portfolio, title="Web Development")
        Service.objects.get_or_create(portfolio=portfolio, title="API Development")
        SocialLink.objects.get_or_create(
            portfolio=portfolio, platform="GitHub", url=f"https://github.com/{username}"
        )