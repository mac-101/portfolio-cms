# API basics

## Base URL

```text
https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG/
```

Replace `YOUR-SLUG` with your portfolio slug. You can change it in **Settings**, but doing so changes every URL below, so update your frontend if you do.

## Endpoints

| Endpoint | Returns |
|---|---|
| `/` | Your profile |
| `/projects/` | Your published projects |
| `/projects/PROJECT-SLUG/` | One published project |
| `/tech-stack/` | Your technologies |
| `/services/` | Your services |
| `/socials/` | Your social links |

Every endpoint accepts `GET` only.

## List responses

List endpoints return an object with the items inside `results`:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": []
}
```

| Field | Meaning |
|---|---|
| `count` | Total number of items |
| `next` | URL of the next page, or `null` |
| `previous` | URL of the previous page, or `null` |
| `results` | The items on this page |

## Pagination

Lists return up to 50 items per page. Use these query parameters:

| Parameter | Example | Meaning |
|---|---|---|
| `page` | `?page=2` | Which page to return |
| `page_size` | `?page_size=100` | Items per page (maximum 100) |

## Errors

| Status | Meaning |
|---|---|
| `404 Not Found` | The slug doesn't exist, or the project is a draft |
| `405 Method Not Allowed` | You used something other than `GET` |

Errors return JSON, for example `{ "detail": "Not found." }`.

## CORS

The API allows `GET` requests from any website, so you can call it directly from browser code.

## Speed and limits

- On free hosting, the first request after a quiet period can take up to a minute while the server wakes up. Show a loading state in your frontend.
- No rate limit is enforced yet, but please cache responses where you can instead of fetching on every page view.

## Helpers used in these docs

The examples in these docs use two small helpers. In plain JavaScript:

```js
const BASE = "https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG";

async function getList(path, params = "") {
  const res = await fetch(`${BASE}/${path}/${params}`);
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return (await res.json()).results;
}
```

In React, save this as `src/lib/api.js` and `src/lib/useList.js`:

```js
// src/lib/api.js
const BASE = import.meta.env.VITE_API_URL;

export async function getList(path, params = "") {
  const res = await fetch(`${BASE}/${path}/${params}`);
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return (await res.json()).results;
}

export async function getProfile() {
  const res = await fetch(`${BASE}/`);
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.json();
}
```

```js
// src/lib/useList.js
import { useEffect, useState } from "react";
import { getList } from "./api";

export function useList(path, params = "") {
  const [state, setState] = useState({ items: [], loading: true, error: null });

  useEffect(() => {
    let cancelled = false;
    getList(path, params)
      .then((items) => !cancelled && setState({ items, loading: false, error: null }))
      .catch((error) => !cancelled && setState({ items: [], loading: false, error }));
    return () => {
      cancelled = true;
    };
  }, [path, params]);

  return state;
}
```