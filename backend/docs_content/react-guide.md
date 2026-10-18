# React

Build a portfolio with React (using Vite) that reads from the API.

## 1. Create the project

```bash
npm create vite@latest my-portfolio -- --template react
cd my-portfolio
npm install
```

## 2. Set your API address

Create a file called `.env` in the project root:

```env
VITE_API_URL=https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG
```

Vite only exposes variables that start with `VITE_`. Restart `npm run dev` after changing this file.

## 3. Add the helpers

Create `src/lib/api.js` and `src/lib/useList.js` with the code from [API basics](/docs/api-basics/#helpers-used-in-these-docs).

## 4. Add an icon component

Tech and service icons are black SVGs. This component paints them in the surrounding text colour, so they match light and dark themes. Save it as `src/components/Icon.jsx`:

```jsx
export default function Icon({ url, label, size = 20 }) {
  const box = { width: size, height: size };

  // No icon set: show the first letter instead of a gap
  if (!url) {
    return (
      <span aria-hidden="true" style={{ ...box, display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: size * 0.6, border: "1px solid currentColor", borderRadius: 4 }}>
        {label.charAt(0)}
      </span>
    );
  }

  return (
    <span
      aria-hidden="true"
      style={{
        ...box,
        display: "inline-block",
        backgroundColor: "currentColor",
        WebkitMaskImage: `url(${url})`,
        maskImage: `url(${url})`,
        WebkitMaskRepeat: "no-repeat",
        maskRepeat: "no-repeat",
        WebkitMaskSize: "contain",
        maskSize: "contain",
        WebkitMaskPosition: "center",
        maskPosition: "center",
      }}
    />
  );
}
```

## 5. Put it together

Replace `src/App.jsx`:

```jsx
import { useEffect, useState } from "react";
import { getProfile } from "./lib/api";
import { useList } from "./lib/useList";
import Icon from "./components/Icon";

export default function App() {
  const [profile, setProfile] = useState(null);
  const projects = useList("projects");
  const skills = useList("tech-stack", "?page_size=100");

  useEffect(() => {
    getProfile().then(setProfile).catch(console.error);
  }, []);

  return (
    <main style={{ maxWidth: 720, margin: "2rem auto", padding: "0 1rem" }}>
      <h1>{profile ? profile.name : "Loading…"}</h1>
      {profile && <p>{profile.bio}</p>}

      <h2>Projects</h2>
      {projects.loading && <p>Loading projects…</p>}
      {projects.error && <p>Couldn't load projects.</p>}
      <ul>
        {projects.items.map((project) => (
          <li key={project.slug}>
            <strong>{project.title}</strong>: {project.description}
          </li>
        ))}
      </ul>

      <h2>Skills</h2>
      <ul style={{ display: "flex", flexWrap: "wrap", gap: "1rem", listStyle: "none", padding: 0 }}>
        {skills.items.map((tech) => (
          <li key={tech.slug} style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <Icon url={tech.icon_url} label={tech.name} />
            {tech.name}
          </li>
        ))}
      </ul>
    </main>
  );
}
```

Run `npm run dev` and open the address it prints.

## Tips

- **Loading and error states matter.** On free hosting, the first request can take up to a minute.
- **Fetch each list once.** If two components need the same data, load it in a parent and pass it down.
- **Look names up for project icons.** Projects return tech names only. Load the tech list once and look icons up by name. See [Using icons](/docs/icons/).