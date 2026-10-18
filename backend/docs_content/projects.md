# Projects

Returns your **published** projects, newest first. Draft projects are never included.

## List projects

```text
GET /projects/
```

| Parameter | Example | Meaning |
|---|---|---|
| `featured` | `?featured=true` | Only featured projects (`false` returns the rest) |
| `page`, `page_size` | `?page_size=100` | See [API basics](/docs/api-basics/) |

## Get one project

```text
GET /projects/PROJECT-SLUG/
```

Returns a single project object. A draft or unknown slug returns `404`.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `title` | string | Project name |
| `slug` | string | URL-friendly name, unique within your portfolio |
| `description` | string | What the project is. May be empty |
| `image` | string or `null` | Full image URL, or `null` if none |
| `tech_stack` | list of strings | Names of the technologies used |
| `github_url` | string | Source code link. May be empty |
| `live_url` | string | Live site link. May be empty |
| `featured` | boolean | Whether you marked it as featured |
| `created_at` | string | When it was created (ISO 8601, UTC) |

## Example response

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
      "image": "https://res.cloudinary.com/your-cloud/image/upload/v1/users/1/projects/abc123.jpg",
      "tech_stack": ["Python", "Django"],
      "github_url": "https://github.com/you/echonote",
      "live_url": "https://example.com/echonote",
      "featured": true,
      "created_at": "2026-10-08T21:14:03Z"
    }
  ]
}
```

## JavaScript and HTML

```html
<ul id="projects"></ul>

<script>
  const BASE = "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG";

  async function showProjects() {
    const res = await fetch(`${BASE}/projects/`);
    const { results } = await res.json();
    const list = document.getElementById("projects");

    for (const project of results) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = project.live_url || "#";
      link.textContent = project.title;       // textContent keeps API data as plain text
      item.append(link, ` · ${project.tech_stack.join(", ")}`);
      list.append(item);
    }
  }

  showProjects();
</script>
```

## React

```jsx
import { useList } from "./lib/useList";

export default function Projects() {
  const { items, loading, error } = useList("projects");

  if (loading) return <p>Loading projects…</p>;
  if (error) return <p>Couldn't load projects.</p>;

  return (
    <ul>
      {items.map((project) => (
        <li key={project.slug}>
          {project.image && <img src={project.image} alt={project.title} width="320" />}
          <h3>{project.title}</h3>
          <p>{project.description}</p>
          <p>{project.tech_stack.join(" · ")}</p>
          {project.live_url && (
            <a href={project.live_url} target="_blank" rel="noopener noreferrer">
              View live
            </a>
          )}
        </li>
      ))}
    </ul>
  );
}
```

To show only featured projects, use `useList("projects", "?featured=true")`.