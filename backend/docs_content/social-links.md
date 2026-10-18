# Social links

Returns the links you've added, in the order you added them.

```text
GET /socials/
```

## Fields

| Field | Type | Meaning |
|---|---|---|
| `platform` | string | Name, such as `GitHub` or `WhatsApp` |
| `url` | string | The link |
| `label` | string | Optional button text, such as `Get a free quote`. May be empty |

## Example response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    { "platform": "GitHub", "url": "https://github.com/you", "label": "" },
    { "platform": "WhatsApp", "url": "https://wa.me/234XXXXXXXXXX", "label": "Get a free quote" }
  ]
}
```

## JavaScript and HTML

```html
<nav id="links"></nav>

<script>
  const BASE = "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG";

  async function showLinks() {
    const res = await fetch(`${BASE}/socials/`);
    const { results } = await res.json();
    const nav = document.getElementById("links");

    for (const link of results) {
      const a = document.createElement("a");
      a.href = link.url;
      a.textContent = link.label || link.platform;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      nav.append(a, " ");
    }
  }

  showLinks();
</script>
```

## React

Use the `label` as button text for a call to action, such as a WhatsApp quote button:

```jsx
import { useList } from "./lib/useList";

export default function Links() {
  const { items } = useList("socials");
  const whatsapp = items.find((link) => link.platform === "WhatsApp");

  return (
    <div>
      {whatsapp && (
        <a href={whatsapp.url} target="_blank" rel="noopener noreferrer">
          {whatsapp.label || "Message me"}
        </a>
      )}
      <ul>
        {items.map((link) => (
          <li key={link.platform}>
            <a href={link.url} target="_blank" rel="noopener noreferrer">
              {link.platform}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```