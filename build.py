"""Build index.html from works.json. Run: python3 build.py
Edit titles, order or years in works.json, then rebuild and push."""
import json, html

REV = "Rev.1"
works = json.load(open("works.json"))

cards = []
for i, w in enumerate(works):
    t = w.get("title") or ""
    alt = f"{t} by Deano" if t else "Untitled work by Deano"
    cap = html.escape(t) if t else ""
    cards.append(
        f'<figure class="card" data-i="{i}">'
        f'<a href="art/full/{w["id"]}.jpg" class="open" aria-label="View {html.escape(alt)}">'
        f'<img src="art/thumb/{w["id"]}.jpg" width="{w["tw"]}" height="{w["th"]}" alt="{html.escape(alt)}" loading="lazy" decoding="async">'
        f'</a>{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>'
    )

data = json.dumps([{"id": w["id"], "t": w.get("title") or ""} for w in works])

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deano | Art by Dean Greenberg</title>
<meta name="description" content="Drawings and paintings by Deano (Dean Greenberg). Bold lines, bright color.">
<meta property="og:title" content="Deano | Art by Dean Greenberg">
<meta property="og:description" content="Drawings and paintings by Deano.">
<meta property="og:image" content="https://deano.art/art/full/{works[0]['id']}.jpg">
<meta property="og:url" content="https://deano.art/">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{
  --ink: #111; --paper: #fbfaf7; --muted: #6b6b6b;
  --red: #e2382b; --yellow: #f5c518; --blue: #1f5fd6; --green: #1e9e57; --pink: #e8559a;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: var(--paper); color: var(--ink); }}
body {{ font: 16px/1.5 Archivo, system-ui, sans-serif; }}
a {{ color: inherit; }}
header {{ padding: 48px 20px 28px; max-width: 1400px; margin: 0 auto; }}
.mark {{ font-family: "Archivo Black", Archivo, sans-serif; font-size: clamp(64px, 14vw, 168px);
  line-height: .85; letter-spacing: -0.03em; margin: 0; display: flex; align-items: flex-end; gap: .08em; }}
.mark span {{ display: inline-block; }}
.dots {{ display: inline-flex; flex: none; gap: .08em; margin-left: .06em; margin-bottom: .04em; font-size: 1em; }}
.dots i {{ display: block; width: .17em; height: .17em; border-radius: 50%; border: .035em solid var(--ink); }}
.dots i:nth-child(1) {{ background: var(--red); }}
.dots i:nth-child(2) {{ background: var(--yellow); }}
.dots i:nth-child(3) {{ background: var(--blue); }}
.dots i:nth-child(4) {{ background: var(--green); }}
.sub {{ margin: 18px 0 0; font-size: clamp(17px, 2.2vw, 21px); max-width: 40ch; }}
.sub b {{ font-weight: 600; }}
nav {{ margin-top: 18px; display: flex; gap: 22px; font-weight: 600; }}
nav a {{ text-decoration: none; border-bottom: 3px solid var(--yellow); }}
nav a:hover {{ border-color: var(--red); }}
main {{ max-width: 1400px; margin: 0 auto; padding: 8px 20px 40px; }}
.grid {{ columns: 3 320px; column-gap: 22px; }}
.card {{ break-inside: avoid; margin: 0 0 22px; }}
.card a {{ display: block; background: #fff; border: 3px solid var(--ink); border-radius: 4px;
  box-shadow: 6px 6px 0 var(--ink); transition: transform .12s, box-shadow .12s; overflow: hidden; }}
.card a:hover, .card a:focus-visible {{ transform: translate(-2px, -2px); box-shadow: 8px 8px 0 var(--ink); outline: none; }}
.card img {{ display: block; width: 100%; height: auto; }}
figcaption {{ margin-top: 10px; font-weight: 600; }}
#about {{ max-width: 760px; margin: 40px auto 0; padding: 32px 20px; border-top: 3px solid var(--ink); }}
#about h2 {{ font-family: "Archivo Black", sans-serif; font-size: 32px; margin: 0 0 12px; }}
footer {{ text-align: center; color: var(--muted); font-size: 14px; padding: 28px 20px 48px; }}
/* lightbox */
.lb {{ position: fixed; inset: 0; background: rgba(17,17,17,.94); display: none; z-index: 10;
  align-items: center; justify-content: center; flex-direction: column; padding: 56px 16px 24px; }}
.lb.on {{ display: flex; }}
.lb img {{ max-width: 100%; max-height: calc(100vh - 140px); object-fit: contain; background: #fff; box-shadow: 0 10px 40px rgba(0,0,0,.5); }}
.lb .cap {{ color: #fff; margin-top: 14px; font-weight: 600; min-height: 1.5em; text-align: center; }}
.lb button {{ position: absolute; background: #fff; color: var(--ink); border: 3px solid var(--ink); border-radius: 50%;
  width: 48px; height: 48px; font: 700 22px/1 Archivo, sans-serif; cursor: pointer; }}
.lb .x {{ top: 12px; right: 12px; }}
.lb .prev {{ left: 12px; top: 50%; transform: translateY(-50%); }}
.lb .next {{ right: 12px; top: 50%; transform: translateY(-50%); }}
.lb button:hover {{ background: var(--yellow); }}
@media (max-width: 600px) {{
  header {{ padding-top: 32px; }}
  .grid {{ columns: 2 150px; column-gap: 14px; }}
  .card {{ margin-bottom: 14px; }}
  .card a {{ border-width: 2px; box-shadow: 4px 4px 0 var(--ink); }}
  figcaption {{ font-size: 14px; }}
  .lb .prev, .lb .next {{ top: auto; bottom: 16px; transform: none; }}
  .lb img {{ max-height: calc(100vh - 170px); }}
}}
</style>
</head>
<body>
<header>
  <h1 class="mark"><span>Deano</span><span class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i></span></h1>
  <p class="sub">Drawings and paintings by <b>Dean Greenberg</b>.</p>
  <nav><a href="#work">Work</a><a href="#about">About</a></nav>
</header>
<main id="work">
  <div class="grid">
{chr(10).join(cards)}
  </div>
</main>
<section id="about">
  <h2>About</h2>
  <p>Deano is the artist name of Dean Greenberg. He works in marker, colored pencil and paint on paper. Many pieces carry his mark, DG, and the year.</p>
</section>
<footer>&copy; <span id="y">2026</span> Dean Greenberg. All rights reserved. &middot; {REV}</footer>

<div class="lb" role="dialog" aria-modal="true" aria-label="Artwork viewer">
  <button class="x" aria-label="Close">&times;</button>
  <button class="prev" aria-label="Previous">&#8592;</button>
  <img alt="">
  <div class="cap"></div>
  <button class="next" aria-label="Next">&#8594;</button>
</div>
<script>
const W = {data};
const lb = document.querySelector('.lb'), im = lb.querySelector('img'), cap = lb.querySelector('.cap');
let cur = 0, last = null;
function show(i) {{
  cur = (i + W.length) % W.length;
  im.src = 'art/full/' + W[cur].id + '.jpg';
  im.alt = W[cur].t ? W[cur].t + ' by Deano' : 'Untitled work by Deano';
  cap.textContent = W[cur].t || '';
  [cur + 1, cur - 1].forEach(j => {{ const p = new Image(); p.src = 'art/full/' + W[(j + W.length) % W.length].id + '.jpg'; }});
}}
function open(i) {{ last = document.activeElement; show(i); lb.classList.add('on'); document.body.style.overflow = 'hidden'; lb.querySelector('.x').focus(); }}
function close() {{ lb.classList.remove('on'); document.body.style.overflow = ''; if (last) last.focus(); }}
document.querySelectorAll('.card').forEach(c => c.querySelector('a').addEventListener('click', e => {{ e.preventDefault(); open(+c.dataset.i); }}));
lb.querySelector('.x').onclick = close;
lb.querySelector('.prev').onclick = () => show(cur - 1);
lb.querySelector('.next').onclick = () => show(cur + 1);
lb.addEventListener('click', e => {{ if (e.target === lb) close(); }});
document.addEventListener('keydown', e => {{
  if (!lb.classList.contains('on')) return;
  if (e.key === 'Escape') close();
  if (e.key === 'ArrowRight') show(cur + 1);
  if (e.key === 'ArrowLeft') show(cur - 1);
}});
let sx = null;
lb.addEventListener('touchstart', e => {{ sx = e.touches[0].clientX; }}, {{ passive: true }});
lb.addEventListener('touchend', e => {{ if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); sx = null; }});
document.getElementById('y').textContent = new Date().getFullYear();
</script>
</body>
</html>
"""
open("public/index.html", "w").write(page)
print(f"index.html built with {len(works)} works ({REV})")
