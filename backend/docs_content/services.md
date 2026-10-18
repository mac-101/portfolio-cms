# Services

Returns the services you offer, in the order you added them.

```text
GET /services/
```

## Fields

| Field | Type | Meaning |
|---|---|---|
| `title` | string | Service name |
| `description` | string | What the service includes. May be empty |
| `icon` | string | Icon key, such as `globe`. May be empty |
| `icon_url` | string | Ready-to-use image URL for the icon. Empty if there's no icon |

## Example response

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "title": "Custom Websites",
      "description": "Fast, mobile-first websites built from scratch to match your brand.",
      "icon": "globe",
      "icon_url": "https://cdn.jsdelivr.net/npm/lucide-static@0/icons/globe.svg"
    }
  ]
}
```

## JavaScript and HTML

```html
<div id="services"></div>

<script>
  const BASE = "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG";

  async function showServices() {
    const res = await fetch(`${BASE}/services/`);
    const { results } = await res.json();
    const box = document.getElementById("services");

    for (const service of results) {
      const card = document.createElement("div");
      const title = document.createElement("h3");
      const text = document.createElement("p");
      title.textContent = service.title;
      text.textContent = service.description;
      card.append(title, text);
      box.append(card);
    }
  }

  showServices();
</script>
```

## React

```jsx
import { useList } from "./lib/useList";

export default function Services() {
  const { items, loading } = useList("services");
  if (loading) return <p>Loading services…</p>;

  return (
    <div>
      {items.map((service) => (
        <article key={service.title}>
          {service.icon_url && <img src={service.icon_url} alt="" width="24" />}
          <h3>{service.title}</h3>
          <p>{service.description}</p>
        </article>
      ))}
    </div>
  );
}
```