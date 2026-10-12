from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from portfolio.models import Portfolio, Project, TechStack
from portfolio.utils import unique_portfolio_slug


PROJECTS = [
    {
        "title": "Style Hub",
        "category": "Fashion E-commerce",
        "description": "Fashion e-commerce platform with product listing, shopping cart, and checkout functionality, order code tracking, and admin dashboard for managing products and orders.",
        "tags": ["React", "Supabase", "Tailwind"],
        "image": "stylehub.png",
        "live_url": "http://stylehub101.netlify.app/",
        "github_url": "https://github.com/mac-101/StyleHub",
        "featured": True,
    },
    {
        "title": "Clever School",
        "category": "Education",
        "description": "A modern, high-performance informational website. It showcases academic programs, campus culture, and admissions to parents and prospective students through a highly accessible, easy-to-navigate interface",
        "tags": ["HTML", "REST API", "CSS", "JavaScript"],
        "image": "cleverschools.png",
        "live_url": "http://cleverkidsschoolsinternational.com.ng/",
        "github_url": "http://github.com/mac-101",
        "featured": True,
    },
    {
        "title": "Hybrid Security Consult",
        "category": "Cybersecurity",
        "description": "(Collaborated) Cybersecurity consulting platform with service offerings, training programs enrollment, client testimonials, contact form for inquiries and admin panel.",
        "tags": ["React", "Node.js", "Tailwind"],
        "image": "hybridsec.png",
        "live_url": "https://www.hybridsecconsult.com/",
        "github_url": "https://github.com/mac-101",
        "featured": True,
    },
    {
        "title": "Essy Kilishi",
        "category": "Brand Site",
        "description": "A beef jerky business site, product showcase, placing order, and gaining trust",
        "tags": ["React", "Tailwind"],
        "image": "essykilishi.png",
        "live_url": "https://essy-kilishi.vercel.app/",
        "github_url": "https://github.com/mac-101/essy-kilishi",
        "featured": False,
    },
    {
        "title": "Smart School OS",
        "category": "School Management",
        "description": "(In production) School management system, staff listing, student listing, timetable scheduling, school curriculum, fees tracking.",
        "tags": ["Django", "Python", "React", "DRF", "PostgreSQL", "Tailwind"],
        "image": "schmanage.png",
        "live_url": "",
        "github_url": "https://github.com/mac-101/school-management-system",
        "featured": True,
    },
    {
        "title": "Glory Bakery & Gallery",
        "category": "Bakery",
        "description": "Online showcase and gallery of cakes with custom orders, team booking slots, and baking academy enrollment.",
        "tags": ["React", "Tailwind"],
        "image": "bakery.png",
        "live_url": "https://glory-bakery.netlify.app/",
        "github_url": "https://github.com/mac-101/glory-bakery",
        "featured": True,
    },
    {
        "title": "PayHaus",
        "category": "Property Management",
        "description": "Rent payment tracking platform helping landlords and tenants manage payments, due dates, and property records.",
        "tags": ["React", "Zustand", "Firebase", "Tailwind"],
        "image": "payhaus.png",
        "live_url": "https://payhaus.netlify.app",
        "github_url": "https://github.com/mac-101/Payhaus",
        "featured": False,
    },
    {
        "title": "BrightPath Academy",
        "category": "Education",
        "description": "A modern, high-performance informational website. It showcases academic programs, campus culture, and admissions to parents and prospective students through a highly accessible, easy-to-navigate interface",
        "tags": ["React", "TypeScript", "Tailwind"],
        "image": "brigthpath.png",
        "live_url": "https://bright-pathacademy.netlify.app",
        "github_url": "https://github.com/mac-101/BrightPath-Academy",
        "featured": False,
    },
    {
        "title": "TastyBite Fast Food",
        "category": "Fast Food",
        "description": "Modern fast food delivery platform with menu management and order tracking.",
        "tags": ["HTML", "CSS", "JavaScript", "Tailwind"],
        "image": "tastybitefastfood.png",
        "live_url": "http://tastybitefastfood.netlify.app",
        "github_url": "https://github.com/mac-101/Tasty-Bite-Restaurant",
        "featured": False,
    },
    {
        "title": "Aba Dev Summit",
        "category": "Event Management",
        "description": "Dev conference event management platform with speaker list, schedule, and registration functionality.",
        "tags": ["HTML", "CSS", "JavaScript", "Tailwind"],
        "image": "abadev.png",
        "live_url": "https://aba-dev-summit.vercel.app/",
        "github_url": "https://github.com/mac-101/Aba-Dev-Summit-2026-landing-page",
        "featured": True,
    },
]


class Command(BaseCommand):
    help = "Add MacAnthony's portfolio projects (and their tech stacks) to a user's portfolio."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="User who will own the projects.")
        parser.add_argument("--images-dir", required=True, help="Folder containing the project screenshots.")
        parser.add_argument(
            "--update", action="store_true",
            help="Overwrite text fields of projects that already exist (default: leave them alone).",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        # ---- Check everything first, so nothing is half-created ----
        try:
            user = User.objects.get(username=options["username"])
        except User.DoesNotExist:
            raise CommandError(
                f'No user named "{options["username"]}". Sign up first, then run this again.'
            )

        images_dir = Path(options["images_dir"]).expanduser()
        if not images_dir.is_dir():
            raise CommandError(f"Images folder not found: {images_dir}")

        missing = [e["image"] for e in PROJECTS if not (images_dir / e["image"]).is_file()]
        if missing:
            raise CommandError(f"Missing images in {images_dir}: {', '.join(missing)}")

        uses_cloudinary = "Cloudinary" in default_storage.__class__.__name__
        has_keys = getattr(settings, "CLOUDINARY_STORAGE", {}).get("API_KEY")
        if uses_cloudinary and not has_keys:
            raise CommandError("Images are stored on Cloudinary, but the Cloudinary keys in .env are empty.")

        portfolio, _ = Portfolio.objects.get_or_create(
            owner=user,
            defaults={"name": user.username, "slug": unique_portfolio_slug(user.username)},
        )

        # Only fill "category" if the Project model has that field.
        has_category = any(f.name == "category" for f in Project._meta.get_fields())

        created = updated = skipped = uploaded = new_tech = 0

        # Newest-first ordering on Project means the LAST one created shows FIRST,
        # so create them in reverse to keep the order of the list above.
        for entry in reversed(PROJECTS):
            slug = slugify(entry["title"])
            fields = {
                "title": entry["title"],
                "description": entry["description"],
                "github_url": entry["github_url"],
                "live_url": entry["live_url"],
                "featured": entry["featured"],
                "published": True,
            }
            if has_category:
                fields["category"] = entry["category"]

            project, was_created = Project.objects.get_or_create(
                portfolio=portfolio, slug=slug, defaults=fields
            )

            if was_created:
                created += 1
            elif options["update"]:
                for key, value in fields.items():
                    setattr(project, key, value)
                project.save()
                updated += 1
            else:
                skipped += 1
                continue

            techs = []
            for name in entry["tags"]:
                tech, tech_created = TechStack.objects.get_or_create(
                    portfolio=portfolio, slug=slugify(name), defaults={"name": name}
                )
                new_tech += int(tech_created)
                techs.append(tech)
            project.tech_stack.set(techs)

            if not project.image:
                source = images_dir / entry["image"]
                with open(source, "rb") as f:
                    project.image.save(source.name, File(f), save=True)
                uploaded += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done for {user.username}: {created} created, {updated} updated, "
            f"{skipped} skipped (already exist), {uploaded} images uploaded, "
            f"{new_tech} tech stack items created."
        ))
        if not has_category:
            self.stdout.write("Note: Project has no category field, so categories were not saved.")