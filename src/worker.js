// deano.art Worker (Rev.6.6)
// Serves the static site from ./public plus the Artist's Entry API.
// Secrets (Cloudflare dashboard > deano-art > Settings > Variables and Secrets, type Secret):
//   ARTIST_PIN  the entry code
//   GH_TOKEN    GitHub fine-grained token, Contents read/write on GH_REPO (for Upload and Publish)

const MAX_FAILS = 6;            // wrong codes allowed per IP...
const WINDOW_MS = 15 * 60e3;    // ...per 15 minutes
const MAX_UPLOAD = 15 * 1024 * 1024;

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

async function locked(env, ip) {
  const r = await env.DB.prepare("SELECT COUNT(*) AS n FROM fails WHERE ip = ? AND ts > ?").bind(ip, Date.now() - WINDOW_MS).first();
  return (r?.n || 0) >= MAX_FAILS;
}

function same(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

async function checkPin(req, env) {
  const ip = req.headers.get("cf-connecting-ip") || "unknown";
  if (!env.ARTIST_PIN) return json({ error: "Artist's Entry is not set up yet." }, 503);
  if (await locked(env, ip)) return json({ error: "Too many tries. Wait 15 minutes." }, 429);
  if (!same(req.headers.get("x-artist-pin") || "", String(env.ARTIST_PIN))) {
    await env.DB.prepare("INSERT INTO fails (ip, ts) VALUES (?, ?)").bind(ip, Date.now()).run();
    await env.DB.prepare("DELETE FROM fails WHERE ts < ?").bind(Date.now() - WINDOW_MS).run();
    return json({ error: "That code isn't right." }, 401);
  }
  return null;
}

// GitHub contents API: create or replace one file on main. body64 is already base64.
async function ghPut(env, path, body64, message) {
  const repo = env.GH_REPO || "intenseone/deano-art";
  const url = `${env.GH_API || "https://api.github.com"}/repos/${repo}/contents/${path}`;
  const headers = {
    authorization: `Bearer ${env.GH_TOKEN}`, accept: "application/vnd.github+json",
    "user-agent": "deano-art-worker", "x-github-api-version": "2022-11-28",
  };
  for (let attempt = 0; attempt < 3; attempt++) {
    let sha = "";
    const head = await fetch(url + "?ref=main", { headers });
    if (head.ok) sha = (await head.json()).sha || "";
    const payload = '{"message":' + JSON.stringify(message) + ',"branch":"main"' + (sha ? ',"sha":"' + sha + '"' : "") + ',"content":"' + body64 + '"}';
    const r = await fetch(url, { method: "PUT", headers: { ...headers, "content-type": "application/json" }, body: payload });
    if (r.ok) return { ok: true };
    if (r.status !== 409 && r.status !== 422) return { ok: false, status: r.status, text: (await r.text()).slice(0, 200) };
    await new Promise(res => setTimeout(res, 800));
  }
  return { ok: false, status: 409, text: "conflict" };
}

const b64 = s => btoa(unescape(encodeURIComponent(s)));

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (!url.pathname.startsWith("/api/artist")) return env.ASSETS.fetch(req);

    const deny = await checkPin(req, env);
    if (deny) return deny;
    const p = url.pathname;

    if (p === "/api/artist/login" && req.method === "POST") return json({ ok: true, canPublish: !!env.GH_TOKEN });

    if (p === "/api/artist/edits" && req.method === "GET") {
      const { results } = await env.DB.prepare("SELECT id, turn, title, hidden, frame, updated FROM edits").all();
      return json({ edits: results });
    }

    const m = p.match(/^\/api\/artist\/edits\/(\d{3,6})$/);
    if (m && req.method === "PUT") {
      let body;
      try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
      const turn = ((Number(body.turn) || 0) % 360 + 360) % 360;
      if (![0, 90, 180, 270].includes(turn)) return json({ error: "Bad turn" }, 400);
      const title = String(body.title ?? "").slice(0, 120).trim();
      const hidden = body.hidden ? 1 : 0;
      const frame = ["fit", "wide", "tall"].includes(body.frame) ? body.frame : "";
      await env.DB.prepare(
        "INSERT INTO edits (id, turn, title, hidden, frame, note, updated) VALUES (?, ?, ?, ?, ?, '', ?) " +
        "ON CONFLICT(id) DO UPDATE SET turn = excluded.turn, title = excluded.title, hidden = excluded.hidden, frame = excluded.frame, updated = excluded.updated"
      ).bind(m[1], turn, title, hidden, frame, new Date().toISOString()).run();
      return json({ ok: true });
    }

    // Upload: body is the image as base64 text; x-file-ext gives the extension.
    if (p === "/api/artist/upload" && req.method === "POST") {
      if (!env.GH_TOKEN) return json({ error: "Uploading is not set up yet." }, 503);
      const ext = (req.headers.get("x-file-ext") || "jpg").toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 5) || "jpg";
      if (!["jpg", "jpeg", "png", "heic", "heif", "webp"].includes(ext)) return json({ error: "Please upload a photo." }, 400);
      const body64 = await req.text();   // client sends clean base64; no per-character work here (CPU limit)
      if (!body64 || !/^[A-Za-z0-9+/]{16}/.test(body64.slice(0, 16))) return json({ error: "Please upload a photo." }, 400);
      if (body64.length * 0.75 > MAX_UPLOAD) return json({ error: "That photo is too large." }, 413);
      const stamp = new Date().toISOString().replace(/[-:T]/g, "").slice(0, 14);
      const name = `inbox/${stamp}-${crypto.randomUUID().slice(0, 6)}.${ext}`;
      const r = await ghPut(env, name, body64, "Artist's Entry: new upload");
      return r.ok ? json({ ok: true }) : json({ error: "Upload failed (" + r.status + "). Try again." }, 502);
    }

    // Publish: send saved edits to the repo; the GitHub Action applies them.
    if (p === "/api/artist/publish" && req.method === "POST") {
      if (!env.GH_TOKEN) return json({ error: "Publishing is not set up yet." }, 503);
      const { results } = await env.DB.prepare("SELECT id, turn, title, hidden, frame, updated FROM edits").all();
      if (!results.length) return json({ ok: true, count: 0 });
      const list = results.map(e => ({ id: e.id, turn: e.turn, title: e.title, hidden: !!e.hidden, ...(e.frame ? { frame: e.frame } : {}) }));
      const stamp = new Date().toISOString().replace(/[-:T.Z]/g, "");
      const r = await ghPut(env, `edits/pending-${stamp}.json`, b64(JSON.stringify(list, null, 1)), `Artist's Entry: publish ${list.length} change(s)`);
      if (!r.ok) return json({ error: "Publish failed (" + r.status + "). Try again." }, 502);
      const last = results.reduce((a, e) => (e.updated > a ? e.updated : a), "");
      await env.DB.prepare("DELETE FROM edits WHERE updated <= ?").bind(last).run();
      return json({ ok: true, count: list.length });
    }
    return json({ error: "Not found" }, 404);
  },
};
