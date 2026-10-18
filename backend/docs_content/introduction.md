# Introduction

{{ product_name }} lets you manage your portfolio content in one place and read it from any website or app through a public REST API.

You add your projects, tech stack, services and links in a dashboard. When you publish them, your own frontend can fetch them as JSON and display them however you like.

```text
Dashboard  →  Your content  →  Public REST API  →  Your website
```

## What you can manage

- **Projects:** title, description, image, tools used, links, and featured and published switches.
- **Tech stack:** technologies with an icon, a category and an optional experience level.
- **Services:** the services you offer, each with an optional icon.
- **Social links:** GitHub, WhatsApp, LinkedIn, or any other link.
- **Profile:** name, bio, photo, location and email.

## What the API gives you

- A **read-only** JSON API. Nobody can change your content through it.
- **Published content only.** Draft projects are never returned.
- **No API key** to manage. Your portfolio slug identifies your content.
- **CORS enabled**, so browser code on any domain can call it.

## Where to go next

- New here? Start with the [Quick start](/docs/quick-start/).
- Need exact fields? See [Projects](/docs/projects/), [Tech stack](/docs/tech-stack/), [Services](/docs/services/), [Social links](/docs/social-links/) and [Portfolio](/docs/portfolio/).
- Want a working page? Follow the [HTML guide](/docs/html-guide/) or the [React guide](/docs/react-guide/).

## Status

{{ product_name }} is an MVP in development. Everything in these docs works today. Planned features are not documented here until they exist.