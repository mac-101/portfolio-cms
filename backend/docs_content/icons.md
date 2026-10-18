# Using icons

Tech stack items and services can each have an icon. The API gives you two fields for it:

| Field | Example | Use it for |
|---|---|---|
| `icon` | `django` | The icon's key. Use it with your own icon library or URL |
| `icon_url` | `https://cdn.jsdelivr.net/npm/simple-icons@15/icons/django.svg` | A ready-to-use image address |

Tech stack icons are brand logos from [Simple Icons](https://simpleicons.org). Service icons are general symbols from [Lucide](https://lucide.dev). Logos belong to their respective owners.

If an item has no icon, both fields are empty strings, so always have a fallback.

## The simple way

```html
<img src="https://cdn.jsdelivr.net/npm/simple-icons@15/icons/django.svg" alt="" width="24">
```

The icons are black, so they disappear on a dark background.

## Matching your theme colours

Use the SVG as a mask, so the icon takes the colour of the surrounding text:

```html
<span class="icon" style="--icon: url('ICON_URL_HERE')"></span>

<style>
  .icon {
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    background-color: currentColor;
    -webkit-mask: var(--icon) center / contain no-repeat;
    mask: var(--icon) center / contain no-repeat;
  }
</style>
```

Replace `ICON_URL_HERE` with `icon_url`. Because the colour is `currentColor`, it follows your text colour, hover states and dark mode automatically. The React guide has the same thing as a component.

## Brand colours

For technology icons only, Simple Icons can return coloured logos from the `icon` key:

```text
https://cdn.simpleicons.org/django          coloured
https://cdn.simpleicons.org/django/white    white
```

This does not work for service icons.

## Icons on project cards

The projects endpoint returns technology names only. To show their icons, load `/tech-stack/` once, build a lookup by name, and use it when you render each project:

```js
const techs = await getList("tech-stack", "?page_size=100");
const byName = Object.fromEntries(techs.map((t) => [t.name, t]));

// later, for each name in project.tech_stack:
const iconUrl = byName[name]?.icon_url;
```