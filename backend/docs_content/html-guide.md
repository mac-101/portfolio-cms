# Plain HTML and JavaScript

A complete portfolio page with no build step, no framework and no installs. Save it as `index.html` and open it in a browser.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My portfolio</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; }
    li { margin-bottom: 0.5rem; }
  </style>
</head>
<body>
  <h1 id="name">Loading…</h1>
  <p id="bio"></p>

  <h2>Projects</h2>
  <ul id="projects"></ul>

  <h2>Skills</h2>
  <ul id="skills"></ul>

  <script>
    const BASE = "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG";

    async function get(path) {
      const res = await fetch(`${BASE}/${path}`);
      if (!res.ok) throw new Error(`Request failed (${res.status})`);
      return res.json();
    }

    async function init() {
      const [profile, projects, skills] = await Promise.all([
        get(""),
        get("projects/"),
        get("tech-stack/?page_size=100"),
      ]);

      document.getElementById("name").textContent = profile.name;
      document.getElementById("bio").textContent = profile.bio;

      for (const project of projects.results) {
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = project.live_url || "#";
        link.textContent = project.title;
        item.append(link, ` · ${project.tech_stack.join(", ")}`);
        document.getElementById("projects").append(item);
      }

      for (const tech of skills.results) {
        const item = document.createElement("li");
        item.textContent = tech.name;
        document.getElementById("skills").append(item);
      }
    }

    init().catch(() => {
      document.getElementById("name").textContent = "Couldn't load the portfolio.";
    });
  </script>
</body>
</html>
```

## How it works

1. `get()` is one small function that fetches a path under your base URL and returns the JSON.
2. `Promise.all` makes the three requests at the same time instead of one after another.
3. The profile is a single object, and the other two return lists in `results`.
4. Text goes in with `textContent`, so the API data is always treated as plain text and never as HTML.

## Next steps

- Add images from `project.image` and icons from `tech.icon_url`.
- Group skills using `tech.category`. See [Tech stack](/docs/tech-stack/).
- Put the files on any static host. See [Deploying your frontend](/docs/deploying/).