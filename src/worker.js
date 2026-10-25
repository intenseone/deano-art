// deano.art Worker (Rev.5)
// Serves the static site from ./public and a small API for the Artist's Entry page.
// The entry code lives in the ARTIST_PIN secret (Cloudflare dashboard), never in this repo.

const MAX_FAILS = 6;            // wrong codes allowed per IP...
const WINDOW_MS = 15 * 60e3;    // ...per 15 minutes

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

async function locked(env, ip) {
  const since = Date.now() - WINDOW_MS;
  const r = await env.DB.prepare("SELECT COUNT(*) AS n FROM fails WHERE ip = ? AND ts > ?").bind(ip, since).first();
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
  const pin = req.headers.get("x-artist-pin") || "";
  if (!same(pin, String(env.ARTIST_PIN))) {
    await env.DB.prepare("INSERT INTO fails (ip, ts) VALUES (?, ?)").bind(ip, Date.now()).run();
    await env.DB.prepare("DELETE FROM fails WHERE ts < ?").bind(Date.now() - WINDOW_MS).run();
    return json({ error: "That code isn't right." }, 401);
  }
  return null;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (!url.pathname.startsWith("/api/artist")) return env.ASSETS.fetch(req);

    const deny = await checkPin(req, env);
    if (deny) return deny;

    // POST /api/artist/login -> confirms the code
    if (url.pathname === "/api/artist/login" && req.method === "POST") return json({ ok: true });

    // GET /api/artist/edits -> all saved changes
    if (url.pathname === "/api/artist/edits" && req.method === "GET") {
      const { results } = await env.DB.prepare("SELECT id, turn, title, note, updated FROM edits").all();
      return json({ edits: results });
    }

    // PUT /api/artist/edits/<id> {turn, title, note}
    const m = url.pathname.match(/^\/api\/artist\/edits\/(\d{3,6})$/);
    if (m && req.method === "PUT") {
      let body;
      try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
      const turn = ((Number(body.turn) || 0) % 360 + 360) % 360;
      if (![0, 90, 180, 270].includes(turn)) return json({ error: "Bad turn" }, 400);
      const title = String(body.title || "").slice(0, 120).trim();
      const note = String(body.note || "").slice(0, 500).trim();
      await env.DB.prepare(
        "INSERT INTO edits (id, turn, title, note, updated) VALUES (?, ?, ?, ?, ?) " +
        "ON CONFLICT(id) DO UPDATE SET turn = excluded.turn, title = excluded.title, note = excluded.note, updated = excluded.updated"
      ).bind(m[1], turn, title, note, new Date().toISOString()).run();
      return json({ ok: true });
    }
    return json({ error: "Not found" }, 404);
  },
};
