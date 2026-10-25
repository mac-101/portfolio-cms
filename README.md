# My Portfolio CMS

**A headless CMS for developer portfolios.** Manage your projects, tech stack, services and links in one dashboard, then fetch them from any frontend through a public REST API.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-A30000)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)

**Live demo:** https://my-portfolio-cms-a0js.onrender.com · **Docs:** https://my-portfolio-cms-a0js.onrender.com/docs/ · **Status:** MVP in development

<!-- Add a screenshot or short GIF here. It's the first thing people look at. -->
![Dashboard](docs/screenshots/dashboard.png)

## Why I built it

Portfolio content changes constantly: new projects, new skills, new links. When that content is hard-coded into a frontend, every small update means editing code and redeploying. I built this so the **content lives in one place and the frontend stays free**. Update a project in the dashboard, and any site built on the API picks it up, whether it's React, Next.js, Astro or plain HTML.

It's also my own portfolio's backend, so I use it myself.

## What it does

- **Dashboard** to create, edit, publish and delete projects, tech stack, services and social links
- **Draft and publish** control: only published projects ever appear in the API
- **Public REST API**, read-only, no API key, CORS enabled
- **Tech stack** with brand icons, categories and experience levels
- **Image uploads** to Cloudinary, organised in a folder per user
- **Public docs site** written in Markdown, with copy-ready JavaScript, HTML and React examples
- **Feedback and contact forms** on the landing page and in the dashboard, with spam protection
- **Responsive UI** with a mobile navigation drawer

## How it works

```mermaid
flowchart LR
    A["Dashboard<br/>Django templates + Tailwind"] --> B[("PostgreSQL")]
    B --> C["Public REST API<br/>Django REST Framework"]
    C --> D["Any frontend<br/>React, Next.js, HTML"]
    A --> E["Cloudinary<br/>image storage"]
```

## API at a glance

```text
GET /api/public/portfolios/<slug>/                  profile
GET /api/public/portfolios/<slug>/projects/         published projects (?featured=true)
GET /api/public/portfolios/<slug>/projects/<slug>/  one published project
GET /api/public/portfolios/<slug>/tech-stack/       technologies
GET /api/public/portfolios/<slug>/services/         services
GET /api/public/portfolios/<slug>/socials/          social links
```

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "title": "EchoNote",
      "slug": "echonote",
      "description": "A Django notes application.",
      "tech_stack": ["Python", "Django"],
      "live_url": "https://example.com/echonote",
      "featured": true
    }
  ]
}
```

Full reference with JavaScript and React examples is in the [docs](https://my-portfolio-cms-a0js.onrender.com/docs/).

## Engineering decisions

- **Ownership by structure, not trust.** Every dashboard query is filtered by `request.user.portfolio`, and the portfolio is never taken from the browser. Changing an ID in a URL returns a 404. Related fields (a project's tech stack choices) are limited to the owner's own records.
- **Read-only by construction.** The public API uses `ListAPIView` and `RetrieveAPIView`, so there is no code path that can create, update or delete. Other methods return 405.
- **Allow-listed output.** Serializers list their fields explicitly. IDs, owners and draft flags never leak, and new model fields stay private until exposed on purpose.
- **Drafts stay private.** Unpublished projects return 404, even to someone who guesses the slug.
- **Slug rules.** Project and tech slugs are unique per portfolio through database constraints. Portfolio slugs avoid reserved route names such as `admin`, `api` and `docs`.
- **Safe uploads.** Images go to per-user Cloudinary folders with random filenames, so users can't overwrite each other's files.
- **Public form protection.** The anonymous feedback form uses a honeypot field and a per-IP rate limit, and submissions are only visible to admins.
- **Production configuration.** Settings come from environment variables, and HTTPS-aware cookie and proxy settings turn on when `DEBUG` is off. Tailwind runs from a CDN in development and as compiled CSS in production.
- **Docs without a docs framework.** The docs are Markdown files rendered by one Django view, with an allow-list of page names so no other file can be opened.

## Tech stack

| Area | Tools |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL |
| Frontend | Django templates, Tailwind CSS, a little vanilla JavaScript |
| Media | Cloudinary |
| Docs | Python-Markdown, highlight.js |
| Hosting | Render, with WhiteNoise and Gunicorn |

## Run it locally

Requires Python, PostgreSQL and Git.

```bash
git clone https://github.com/mac-101/portfolio-cms.git
cd portfolio-cms

python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux:  source venv/bin/activate

cd backend
pip install -r requirements.txt
```

Create a PostgreSQL database, then create `backend/.env`:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/DATABASE_NAME
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://localhost:8000`. Image uploads need Cloudinary keys; everything else works without them.

### Optional: demo data

```bash
python manage.py seed_demo
```

Creates two demo users (`macanthony` and `john`) with sample portfolios, which is useful for checking that one user can't see another's data. The demo password is for local development only.

## Environment variables

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local development only |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `DATABASE_URL` | PostgreSQL connection string |
| `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | Image storage |
| `CSRF_TRUSTED_ORIGINS` | Extra trusted `https://` origins, such as a custom domain |
| `CONTACT_EMAIL`, `CONTACT_GITHUB` | Shown on the dashboard Contact page |
| `PRODUCT_NAME` | Display name used in the docs |

## Project structure

```text
backend/
├── config/          settings and root URLs
├── accounts/        signup, login, logout
├── portfolio/       models, dashboard views, forms, seed commands
├── api/             public REST API (serializers, views, pagination)
├── landing/         landing page, feedback, docs renderer
├── docs_content/    the docs, as Markdown files
├── templates/       dashboard, landing and docs templates
└── static/          Tailwind source
```

## Roadmap

- Catalog Library: reusable content types such as experience, education and certifications
- A hosted public portfolio page for people who don't want to build a frontend
- Automated tests for ownership isolation and the public API
- Cleanup of orphaned images when projects are deleted or replaced
- API rate limiting and optional API keys

## About me

Built by **MacAnthony**, a Python and web developer.

- GitHub: [mac-101](https://github.com/mac-101)
- Portfolio: [MacAnthony Charles](https://macanthonycharles.vercel.app)
- LinkedIn: [MacAnthony Charles](https://www.linkedin.com/in/macanthony-charles-561810367?utm_source=share_via&utm_content=profile&utm_medium=member_android)
- Email: charlesmacanthony797@gmail.com

## License

All rights reserved.
