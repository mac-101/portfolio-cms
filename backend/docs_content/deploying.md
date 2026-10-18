# Deploying your frontend

Your frontend is a normal website, so you can host it anywhere. Netlify, Vercel and GitHub Pages all work.

## Plain HTML

Upload your files, or connect a repository, and the host serves them. Your API address is in the page's JavaScript, so there's nothing else to set up.

## React (Vite)

1. Push your project to GitHub.
2. Create a new site on Netlify or Vercel and import the repository.
3. Add an environment variable named `VITE_API_URL` with your base URL:

```text
https://YOUR-DOMAIN/api/public/portfolios/YOUR-SLUG
```

4. Deploy.

Vite writes environment variables into the built files, so if you change `VITE_API_URL` later you need to **redeploy** for the change to take effect.

## Things to check

- **Use `https://`.** A page served over HTTPS can't call an `http://` API address; the browser blocks it.
- **No CORS setup needed.** The API already allows requests from any website.
- **Changed your slug?** Update `VITE_API_URL` and redeploy.
- **New content not showing up?** Make sure the project is published, then refresh. Hosts and browsers can cache responses for a short while.