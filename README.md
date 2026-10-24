# deano.art (Rev.1)

Static gallery site for Deano (Dean Greenberg). Hosted on Cloudflare Pages, deployed from this repo.

## Update the site
1. Edit `works.json` to change titles or order. Each entry is one artwork. `id` matches the files in `public/art/full` and `public/art/thumb`.
2. Run `python3 build.py` to regenerate `public/index.html`.
3. Commit and push to `main`. Cloudflare Pages deploys in about a minute.

## Add new artwork
Add a 2000px-wide JPG to `public/art/full/<id>.jpg` and a 640px JPG to `public/art/thumb/<id>.jpg`, add an entry to `works.json`, rebuild, push.

## Cloudflare settings
Deployed as a Cloudflare Worker with static assets. `wrangler.jsonc` points the Worker at `./public`.
- Build command: (empty)
- Deploy command: `npx wrangler deploy`
- Custom domains: `deano.art`, `www.deano.art` (Settings > Domains & Routes)
