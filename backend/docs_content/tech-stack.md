# Tech stack

Returns the technologies you've added, sorted by name.

```text
GET /tech-stack/
```

## Fields

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Technology name |
| `slug` | string | URL-friendly name |
| `icon` | string | Icon key, such as `django`. May be empty |
| `experience_level` | number or `null` | Your own rating from 0 to 100, or `null` if not set |
| `category` | string or `null` | One of `frontend`, `backend`, `database`, `devops`, `tools`, `design`, `other`, or `null` |
| `icon_url` | string | Ready-to-use image URL for the icon. Empty if there's no icon |

## Example response

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "name": "Django",
      "slug": "django",
      "icon": "django",
      "experience_level": 80,
      "category": "backend",
      "icon_url": "https://cdn.jsdelivr.net/npm/simple-icons@15/icons/django.svg"
    }
  ]
}
```

`experience_level` can be `null`. Check with `!= null`, not truthiness, because `0` is a real value.

## JavaScript and HTML

```html
<ul id="skills"></ul>

<script>
  const BASE = "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG";

  async function showSkills() {
    const res = await fetch(`${BASE}/tech-stack/?page_size=100`);
    const { results } = await res.json();
    const list = document.getElementById("skills");

    for (const tech of results) {
      const item = document.createElement("li");

      if (tech.icon_url) {
        const img = document.createElement("img");
        img.src = tech.icon_url;
        img.alt = "";
        img.width = 20;
        item.append(img, " ");
      }

      const level = tech.experience_level != null ? ` (${tech.experience_level}%)` : "";
      item.append(tech.name + level);
      list.append(item);
    }
  }

  showSkills();
</script>
```

## React

Group technologies by category and draw a skill bar when a level is set:

```jsx
import { useList } from "./lib/useList";

const LABELS = {
  frontend: "Frontend",
  backend: "Backend",
  database: "Database",
  devops: "DevOps & Hosting",
  tools: "Tools",
  design: "Design",
  other: "Other",
};

export default function Skills() {
  const { items, loading } = useList("tech-stack", "?page_size=100");
  if (loading) return <p>Loading skills…</p>;

  const groups = {};
  for (const tech of items) {
    (groups[tech.category ?? "other"] ??= []).push(tech);
  }

  return (
    <div>
      {Object.entries(LABELS)
        .filter(([key]) => groups[key])
        .map(([key, label]) => (
          <section key={key}>
            <h3>{label}</h3>
            <ul>
              {groups[key].map((tech) => (
                <li key={tech.slug}>
                  {tech.icon_url && <img src={tech.icon_url} alt="" width="20" />} {tech.name}
                  {tech.experience_level != null && (
                    <progress value={tech.experience_level} max="100" />
                  )}
                </li>
              ))}
            </ul>
          </section>
        ))}
    </div>
  );
}
```

For icons that follow your theme colours, see [Using icons](/docs/icons/).