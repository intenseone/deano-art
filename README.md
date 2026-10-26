# deano.art (Rev.8)

Static gallery site for Deano (Dean Greenberg). Hosted on Cloudflare Workers static assets, deployed from this repo.

## Update the site
1. Edit `works.json` to change titles or order. Each entry is one artwork. `id` matches the files in `public/art/full` and `public/art/thumb`.
2. Run `python3 build.py` to regenerate `public/index.html`.
3. Commit and push to `main`. Cloudflare deploys in about a minute.

## Add new artwork
Add a 2000px-wide JPG to `public/art/full/<id>.jpg` and a 640px JPG to `public/art/thumb/<id>.jpg`, add an entry to `works.json`, rebuild, push.

## Cloudflare settings
Deployed as a Cloudflare Worker with static assets. `wrangler.jsonc` points the Worker at `./public`.
- Build command: (empty)
- Deploy command: `npx wrangler deploy`
- Custom domains: `deano.art`, `www.deano.art` (Settings > Domains & Routes)

## Pages (Rev.3)
`python3 build.py` builds all pages from `works.json`:
- `/` gallery wall (home), with wall color and shuffle
- `/one/` one at a time, background tinted per piece
- `/rooms/` grouped by `room`: shapes, paint, lines, people
Every page has a "View the gallery as" switcher. Old `/preview/` links redirect via `public/_redirects`.

## Artist's Entry (Rev.6)
`/artist/` (code-protected). Dean can turn, name and hide pieces, publish, and upload new photos.
- Secrets on the Worker (type Secret): `ARTIST_PIN`, `GH_TOKEN` (fine-grained, Contents read/write on this repo).
- Saved edits live in D1 `deano-art`. **Publish** writes `edits/pending-*.json`; **Upload** writes `inbox/*`.
- `.github/workflows/apply.yml` runs `tools/apply.py`: crops uploads (`tools/crop.py`), applies edits, rebuilds, commits. Originals go to `originals/`.
- Pieces with `"hidden": true` in `works.json` stay off public pages but still show in Artist's Entry.
- `"frame": "wide" | "tall"` puts a piece in a 4:3 or 3:4 frame with extra mat on the gallery wall (Rev.6.6). Missing or `"fit"` = frame matches the art.
- **Adjust corners** (Rev.8): uploads keep `originals/<id>.*` plus a 1600px preview in `public/art/orig/`. In Artist's Entry the dots start at the auto-crop (`quad` in `works.json`, fractions TL, TR, BR, BL). Saved corners publish as `corners`; `tools/apply.py` re-crops from the original, then applies `rot` and any new turn.
