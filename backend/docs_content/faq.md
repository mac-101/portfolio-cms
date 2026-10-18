# FAQ and troubleshooting

## My project returns 404

Check that **Published** is ticked on the project. Drafts return `404` on purpose. Also check the project slug in the URL, which you can see on the project's page in the dashboard.

## My project isn't in the list

The list only includes published projects. If you have more than 50, add `?page_size=100` or follow the `next` link.

## The first request is very slow

On free hosting the server goes to sleep after a quiet period, and the first request wakes it up, which can take up to a minute. Later requests are fast. Show a loading state so visitors aren't looking at a blank page.

## Images don't show

- Open the `image` URL directly in your browser to check that it loads.
- An empty image comes back as `null`. Check before rendering an `<img>`.
- Make sure you uploaded an image on the project's edit page.

## An icon doesn't show

- The item may have no icon. `icon_url` is an empty string then, so use a fallback.
- Open the `icon_url` in your browser to see whether it loads.
- Icons are black SVGs, so they're invisible on dark backgrounds unless you use the mask technique in [Using icons](/docs/icons/).

## I get a CORS error

The API allows `GET` requests from any site. Check that you're using the exact URL from your dashboard, that it's `https://`, and that you aren't sending custom headers or other request methods.

## `experience_level` shows `0` or nothing

`null` means you haven't set a level. `0` is a real value. In JavaScript, check `tech.experience_level != null`, not just whether it's truthy.

## Can I change content through the API?

No. The API is read-only. Edit your content in the dashboard.

## Is there an API key or rate limit?

Not yet. Your slug identifies your content, and no rate limit is enforced. Please cache responses where you can.

## Something else is wrong

Use the [feedback form](/feedback/) and tell us what you were trying to do.