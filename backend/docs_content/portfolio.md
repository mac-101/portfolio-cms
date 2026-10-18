# Portfolio

Returns your public profile. This is the base URL itself, with no extra path.

```text
GET /
```

## Fields

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Your display name |
| `slug` | string | Your portfolio slug |
| `bio` | string | Your introduction. May be empty |
| `profile_image` | string or `null` | Full image URL, or `null` if none |
| `location` | string | Where you're based. May be empty |
| `email` | string | Contact email. May be empty |

The email is public. Leave it blank in **Settings** if you don't want it returned.

## Example response

```json
{
  "name": "MacAnthony",
  "slug": "macanthony",
  "bio": "Python and web developer building useful things for the web.",
  "profile_image": null,
  "location": "Aba, Nigeria",
  "email": ""
}
```

This endpoint returns a single object, not a `results` list.

## JavaScript and HTML

```html
<h1 id="name"></h1>
<p id="bio"></p>

<script>
  const BASE = "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG";

  async function showProfile() {
    const res = await fetch(`${BASE}/`);
    const profile = await res.json();
    document.getElementById("name").textContent = profile.name;
    document.getElementById("bio").textContent = profile.bio;
  }

  showProfile();
</script>
```

## React

```jsx
import { useEffect, useState } from "react";
import { getProfile } from "./lib/api";

export default function Profile() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    getProfile().then(setProfile).catch(console.error);
  }, []);

  if (!profile) return null;

  return (
    <header>
      {profile.profile_image && <img src={profile.profile_image} alt={profile.name} width="96" />}
      <h1>{profile.name}</h1>
      <p>{profile.bio}</p>
    </header>
  );
}
```