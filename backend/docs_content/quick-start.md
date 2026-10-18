# Quick start

Get your first API response in about five minutes.

## 1. Create an account

Sign up and log in. A portfolio is created for you automatically, with a slug based on your username.

## 2. Add your content

In the dashboard sidebar:

1. **Projects:** click **Add Project**, fill in the details, and tick **Published**.
2. **Tech Stack:** add the technologies you use and pick an icon for each.
3. **Services** and **Socials:** add what you offer and where people can find you.

Projects are saved as drafts unless **Published** is ticked. Drafts are not returned by the API.

## 3. Find your API address

Open **API** in the dashboard sidebar. Your base URL looks like this:

```text
https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG/
```

## 4. Make your first request

Paste the projects URL into your browser:

```text
https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG/projects/
```

Or use `curl`:

```bash
curl "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG/projects/"
```

You should get JSON like this:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    { "title": "EchoNote", "slug": "echonote", "tech_stack": ["Python", "Django"] }
  ]
}
```

## 5. Show it on a page

Follow the [HTML guide](/docs/html-guide/) or the [React guide](/docs/react-guide/).