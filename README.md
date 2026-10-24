# deano.art (Rev.1)

Static gallery site for Deano (Dean Greenberg). Hosted on Cloudflare Pages, deployed from this repo.

## Update the site
1. Edit `works.json` to change titles or order. Each entry is one artwork. `id` matches the files in `art/full` and `art/thumb`.
2. Run `python3 build.py` to regenerate `index.html`.
3. Commit and push to `main`. Cloudflare Pages deploys in about a minute.

## Add new artwork
Add a 2000px-wide JPG to `art/full/<id>.jpg` and a 640px JPG to `art/thumb/<id>.jpg`, add an entry to `works.json`, rebuild, push.

## Cloudflare Pages settings
- Framework preset: None
- Build command: (empty)
- Build output directory: `/`
- Custom domains: `deano.art`, `www.deano.art`
