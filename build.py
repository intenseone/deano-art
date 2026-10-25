"""Build deano.art from works.json. Run: python3 build.py
Pages: / (gallery wall), /one/ (one at a time), /rooms/ (rooms).
Edit titles, order, room or colors in works.json, then rebuild and push."""
import json, os, html

REV = "Rev.5.1"
works = json.load(open("works.json"))
DATA = json.dumps([{
    "id": w["id"], "t": w.get("title") or "", "w": w["w"], "h": w["h"], "tw": w["tw"], "th": w["th"],
    "p": w["palette"][:3], "room": w["room"],
} for w in works], separators=(",", ":"))

ABOUT = [
    "Dean Greenberg grew up in Saint Paul, Minnesota. He started out in the scrap business, moved into meat processing, "
    "and went on to run Newport Cold Storage in Saint Paul. He has also backed many startups as an investor.",
    "He has collected art for 50 years. His collection includes Joan Mir\u00f3 and Alexander Calder, along with many sculptures. "
    "A few years ago he picked up a set of markers and started making his own.",
    "He works at home with no plan. He starts with a line and lets the piece find its shape, and he calls every one of them a doodle. "
    "The collector shows in the work: heavy black lines, floating shapes and flat, bright color that recall Mir\u00f3 and Calder. "
    "He moves between marker, colored pencil and paint, and he keeps trying new materials.",
    "Deano has never shown his work in a gallery. He makes art because it is therapeutic and because it lets him explore new worlds. "
    "Most pieces go to family and friends, and many arrive by text message.",
]
OG_IMG = "https://deano.art/art/full/9294.jpg"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="Doodles by Deano (Dean Greenberg). Bold lines, bright color.">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="Doodles by Deano (Dean Greenberg).">
<meta property="og:image" content="__OG__">
<meta property="og:url" content="https://deano.art__PATH__">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://deano.art__PATH__">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/base.css">
<style>__CSS__</style>
</head>
<body>
"""
MARK = '<a class="mark" href="/" aria-label="Deano home">Deano<span class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i></span></a>'
VIEWS = [("/", "Gallery wall", "Wall"), ("/one/", "One at a time", "One at a time"), ("/rooms/", "Rooms", "Rooms")]

def switcher(cur):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == cur else ""}>'
        f'<span class="long">{long}</span><span class="short">{short}</span></a>'
        for href, long, short in VIEWS)
    return f'<nav class="views" aria-label="View the gallery as"><span class="vl">View the gallery as</span><div class="seg">{links}</div></nav>'

def page(path, title, css, body, js):
    head = HEAD if path != "/artist/" else HEAD.replace("<title>", '<meta name="robots" content="noindex, nofollow">\n<title>', 1)
    out = (head.replace("__TITLE__", title).replace("__CSS__", css)
           .replace("__OG__", OG_IMG).replace("__PATH__", path)) + body
    out += '\n<script src="/assets/viewer.js"></script>\n<script>\nconst W = ' + DATA + ';\n' + js + '\n</script>\n'
    out += f'<!-- {REV} -->\n</body>\n</html>\n'
    d = "public" + path
    os.makedirs(d, exist_ok=True)
    open(d + "index.html", "w").write(out)

FOOT = f'<footer class="foot">&copy; <span class="yr">2026</span> Dean Greenberg. All rights reserved. &middot; {REV} &middot; <a href="/artist/" style="color:inherit">Artist&rsquo;s entry</a></footer>'
YEAR_JS = "document.querySelectorAll('.yr').forEach(e => e.textContent = new Date().getFullYear());"

# ---------------------------------------------------------------- / Gallery wall
page("/", "Deano | Doodles by Dean Greenberg", """
body { --wall: #24344d; --fg: #f6f1e7; background-color: var(--wall); color: var(--fg); transition: background-color .5s, color .5s; min-height: 100vh;
  background-image: radial-gradient(ellipse at 50% -10%, rgba(255,255,255,.14), transparent 60%); }
body.light { --fg: #111; }
header { max-width: 1300px; margin: 0 auto; padding: 36px 20px 6px; display: flex; flex-wrap: wrap; align-items: flex-end; gap: 18px 32px; }
header .mark { font-size: clamp(56px, 10vw, 120px); color: var(--fg); }
header .mark .dots i { border-color: var(--fg); }
header .intro { flex: 1 1 260px; }
header .intro p { margin: 0 0 12px; font-size: clamp(17px, 2vw, 20px); }
.views { color: var(--fg); }
.views .vl { color: var(--fg); }
.tools { max-width: 1300px; margin: 0 auto; padding: 14px 20px 0; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.tools .lbl { font-weight: 600; font-size: 14px; opacity: .85; margin-right: 2px; }
.sw-btn { width: 32px; height: 32px; border-radius: 50%; border: 3px solid var(--fg); cursor: pointer; padding: 0; }
.sw-btn[aria-pressed="true"] { outline: 3px solid var(--yellow); outline-offset: 2px; }
.tools .chip { margin-left: 6px; }
.wall { max-width: 1400px; margin: 0 auto; padding: 36px 20px 60px; display: flex; flex-wrap: wrap;
  justify-content: center; align-items: center; gap: clamp(22px, 4vw, 54px); }
.fr { --r: 0deg; width: var(--sz); transform: rotate(var(--r)); transition: transform .25s, box-shadow .25s;
  background: #fff; padding: calc(var(--sz) * .06); border: clamp(6px, 1vw, 11px) solid #111;
  box-shadow: 0 18px 30px rgba(0,0,0,.45), 0 3px 6px rgba(0,0,0,.3); cursor: zoom-in; display: block; text-decoration: none; }
.fr:hover, .fr:focus-visible { transform: rotate(0deg) scale(1.04); box-shadow: 0 26px 44px rgba(0,0,0,.55); outline: none; z-index: 2; position: relative; }
.fr img { width: 100%; height: auto; }
.fr.s { --sz: clamp(130px, 17vw, 220px); } .fr.m { --sz: clamp(150px, 23vw, 300px); } .fr.l { --sz: clamp(170px, 31vw, 420px); }
.plate { display: block; margin-top: 8px; font: 600 12px/1.2 Archivo, sans-serif; color: #111; text-align: center; letter-spacing: .02em; }
#about { max-width: 760px; margin: 0 auto; padding: 34px 20px 10px; border-top: 3px solid var(--fg); }
#about h2 { font-family: "Archivo Black", sans-serif; font-size: 32px; margin: 0 0 12px; }
#about p { font-size: 18px; line-height: 1.6; margin: 0 0 14px; }
.foot { text-align: center; opacity: .7; font-size: 14px; padding: 26px 20px 40px; }
@media (max-width: 600px) { .fr.s, .fr.m, .fr.l { --sz: 40vw; } .wall { gap: 26px 18px; } }
""", f"""
<header>
  {MARK}
  <div class="intro"><p>Doodles by <b>Dean Greenberg</b>. <a class="ab" href="#about">About Deano</a></p>{switcher("/")}</div>
</header>
<div class="tools">
  <span class="lbl">Wall color</span>
  <button class="sw-btn" data-wall="#24344d" style="background:#24344d" aria-label="Deep blue wall" aria-pressed="true"></button>
  <button class="sw-btn" data-wall="#2b2b2b" style="background:#2b2b2b" aria-label="Charcoal wall" aria-pressed="false"></button>
  <button class="sw-btn" data-wall="#8c2f2a" style="background:#8c2f2a" aria-label="Red wall" aria-pressed="false"></button>
  <button class="sw-btn" data-wall="#e9e2d3" data-light="1" style="background:#e9e2d3" aria-label="Cream wall" aria-pressed="false"></button>
  <button class="chip" id="shuffle">Shuffle the wall</button>
</div>
<main class="wall" id="wall"></main>
<section id="about"><h2>About Deano</h2>{"".join("<p>" + html.escape(p) + "</p>" for p in ABOUT)}</section>
{FOOT}
""", """
const wall = document.getElementById('wall'); const viewer = DeanoViewer(W);
function rnd(seed) { let x = Math.sin(seed) * 10000; return x - Math.floor(x); }
let order = W.map((w, i) => i);
function render(seedBase) {
  wall.innerHTML = '';
  order.forEach((i, k) => {
    const w = W[i], r = rnd(+w.id + seedBase);
    const a = document.createElement('a');
    a.href = '/art/full/' + w.id + '.jpg';
    a.className = 'fr ' + (r < .3 ? 's' : r < .75 ? 'm' : 'l');
    a.style.setProperty('--r', ((rnd(+w.id * 7 + seedBase) - .5) * 4).toFixed(2) + 'deg');
    a.setAttribute('aria-label', 'View ' + (w.t || 'untitled work'));
    a.innerHTML = '<img src="/art/thumb/' + w.id + '.jpg" width="' + w.tw + '" height="' + w.th + '" alt="' + (w.t ? w.t + ' by Deano' : 'Untitled work by Deano') + '" loading="lazy" decoding="async">' + (w.t ? '<span class="plate">' + w.t + '</span>' : '');
    a.onclick = e => { e.preventDefault(); viewer.open(k, order.map(j => W[j])); };
    wall.appendChild(a);
  });
}
render(0);
document.getElementById('shuffle').onclick = () => {
  for (let i = order.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; }
  render(Math.floor(Math.random() * 1000));
};
function setWall(b) {
  document.body.style.setProperty('--wall', b.dataset.wall);
  document.body.classList.toggle('light', !!b.dataset.light);
  document.querySelectorAll('.sw-btn').forEach(x => x.setAttribute('aria-pressed', x === b));
  try { localStorage.setItem('deano-wall', b.dataset.wall); } catch (e) {}
}
document.querySelectorAll('.sw-btn').forEach(b => b.onclick = () => setWall(b));
try { const s = localStorage.getItem('deano-wall'); const b = s && document.querySelector('.sw-btn[data-wall="' + s + '"]'); if (b) setWall(b); } catch (e) {}
""" + YEAR_JS)

# ---------------------------------------------------------------- /one/ One at a time
page("/one/", "One at a time | Deano", """
html { scroll-snap-type: y mandatory; }
body { transition: background-color .7s ease; }
.topbar { position: fixed; top: 0; left: 0; right: 0; z-index: 10; display: flex; align-items: center; justify-content: space-between;
  gap: 12px; padding: 12px 16px; }
.topbar .mark { font-size: 30px; }
.topbar .views .vl { display: none; }
.slide { height: 100vh; height: 100svh; scroll-snap-align: start; display: flex; flex-direction: column;
  align-items: center; justify-content: center; padding: 76px 16px 40px; position: relative; }
.intro .big { font-size: clamp(72px, 16vw, 200px); }
.intro p { font-size: clamp(18px, 2.4vw, 24px); margin: 22px 0 0; text-align: center; }
.intro .hint { margin-top: 40px; font-weight: 600; animation: bob 1.6s ease-in-out infinite; }
@keyframes bob { 50% { transform: translateY(8px); } }
.slide figure { margin: 0; display: flex; flex-direction: column; align-items: center; max-width: 100%; }
.slide img { max-height: calc(100svh - 190px); max-width: min(92vw, 1300px); width: auto; height: auto; background: #fff;
  border: 4px solid #111; box-shadow: 10px 10px 0 #111; cursor: zoom-in; }
.slide figcaption { margin-top: 22px; font-weight: 600; font-size: 17px; text-align: center; }
.slide figcaption .n { opacity: .6; font-weight: 400; margin-left: 8px; }
.progress { position: fixed; top: 0; left: 0; height: 5px; background: #111; width: 0; z-index: 11; transition: width .3s; }
@media (max-width: 600px) { .slide img { box-shadow: 6px 6px 0 #111; border-width: 3px; max-height: calc(100svh - 200px); }
  .topbar .mark { font-size: 22px; } .topbar { padding: 10px 10px; } }
""", f"""
<div class="progress" id="prog"></div>
<div class="topbar">{MARK}{switcher("/one/")}</div>
<section class="slide intro" data-bg="#fbfaf7">
  <span class="mark big">Deano<span class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i></span></span>
  <p>Doodles by Dean Greenberg. <a class="ab" href="/#about">About Deano</a></p>
  <div class="hint">Scroll to see all <span id="cnt"></span> pieces, one at a time &darr;</div>
</section>
<main id="slides"></main>
""", """
const box = document.getElementById('slides'); const viewer = DeanoViewer(W);
document.getElementById('cnt').textContent = W.length;
function tint(hex, amt) {
  const n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
  const m = c => Math.round(c + (255 - c) * amt);
  return 'rgb(' + m(r) + ',' + m(g) + ',' + m(b) + ')';
}
W.forEach((w, i) => {
  const s = document.createElement('section');
  s.className = 'slide'; s.dataset.bg = tint(w.p[0] || '#888888', .72); s.dataset.i = i;
  s.innerHTML = '<figure><img src="/art/full/' + w.id + '.jpg" width="' + w.w + '" height="' + w.h + '" alt="' + (w.t ? w.t + ' by Deano' : 'Untitled work by Deano') + '" loading="lazy" decoding="async"><figcaption>' + (w.t || 'Untitled') + '<span class="n">' + (i + 1) + ' / ' + W.length + '</span></figcaption></figure>';
  s.querySelector('img').onclick = () => viewer.open(i);
  box.appendChild(s);
});
const io = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return;
  document.body.style.backgroundColor = e.target.dataset.bg;
  const i = e.target.dataset.i;
  document.getElementById('prog').style.width = i === undefined ? 0 : ((+i + 1) / W.length * 100) + '%';
}), { threshold: .55 });
document.querySelectorAll('.slide').forEach(s => io.observe(s));
document.addEventListener('keydown', e => {
  if (document.querySelector('.dv.on')) return;
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); scrollBy({ top: innerHeight, behavior: 'smooth' }); }
  if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); scrollBy({ top: -innerHeight, behavior: 'smooth' }); }
});
""")

# ---------------------------------------------------------------- /rooms/ Rooms
ROOMS = [
    ("shapes", "Bold Shapes", "Thick black outlines and solid color.", ["#e2382b", "#f5c518", "#1f5fd6", "#1e9e57"]),
    ("paint", "Paint", "Brush, sponge and watercolor.", ["#1f5fd6", "#e8559a", "#f39c3d", "#7cc0d8"]),
    ("lines", "Lines and Scribbles", "Loops, zigzags and layered line.", ["#111", "#e2382b", "#1f5fd6", "#111"]),
    ("people", "People and Places", "Faces, buildings, trees and water.", ["#1e9e57", "#7cc0d8", "#c9884a", "#f5c518"]),
]
room_nav = "".join(f'<a class="chip" href="#{k}">{n} <span class="ct" data-room="{k}"></span></a>' for k, n, _, _ in ROOMS)
room_secs = "".join(
    f'<section class="room" id="{k}"><div class="band">' + "".join(f'<i style="background:{c}"></i>' for c in cols) +
    f'</div><h2>{n}</h2><p class="desc">{d}</p><div class="row" data-room="{k}"></div></section>'
    for k, n, d, cols in ROOMS)
page("/rooms/", "Rooms | Deano", """
header { max-width: 1400px; margin: 0 auto; padding: 36px 20px 8px; display: flex; flex-wrap: wrap; align-items: flex-end; gap: 18px 32px; }
header .mark { font-size: clamp(56px, 10vw, 120px); }
header .intro { flex: 1 1 260px; }
header .intro p { margin: 0 0 12px; font-size: clamp(17px, 2vw, 20px); }
.rnav { position: sticky; top: 0; z-index: 5; background: rgba(251,250,247,.94); backdrop-filter: blur(6px);
  border-bottom: 3px solid #111; margin-top: 16px; }
.rnav div { max-width: 1400px; margin: 0 auto; padding: 12px 20px; display: flex; gap: 10px; overflow-x: auto; }
.rnav .ct { opacity: .6; font-weight: 400; }
.room { max-width: 1400px; margin: 0 auto; padding: 46px 20px 10px; scroll-margin-top: 70px; }
.band { display: flex; height: 16px; border: 3px solid #111; width: min(320px, 70%); margin-bottom: 18px; }
.band i { flex: 1; } .band i + i { border-left: 3px solid #111; }
.room h2 { font-family: "Archivo Black", sans-serif; font-size: clamp(30px, 5vw, 52px); line-height: 1; margin: 0; }
.desc { margin: 10px 0 24px; color: #444; }
.row { display: flex; flex-wrap: wrap; gap: 16px; }
.row::after { content: ""; flex-grow: 999; }
.tile { display: block; position: relative; background: #fff; border: 3px solid #111; overflow: hidden; cursor: zoom-in;
  transition: transform .12s, box-shadow .12s; }
.tile img { width: 100%; height: 100%; object-fit: cover; }
.tile:hover { box-shadow: 6px 6px 0 #111; transform: translate(-2px,-2px); }
.tile .t { position: absolute; left: 0; bottom: 0; background: #111; color: #fff; font: 600 12px/1 Archivo, sans-serif; padding: 6px 8px; }
.foot { text-align: center; color: #6b6b6b; font-size: 14px; padding: 40px 20px 40px; }
@media (max-width: 600px) { .row { gap: 10px; } .tile { border-width: 2px; } }
""", f"""
<header>{MARK}<div class="intro"><p>Doodles by <b>Dean Greenberg</b>, grouped by how they were made. <a class="ab" href="/#about">About Deano</a></p>{switcher("/rooms/")}</div></header>
<nav class="rnav" aria-label="Rooms"><div>{room_nav}</div></nav>
{room_secs}
{FOOT}
""", """
const viewer = DeanoViewer(W);
const H = matchMedia('(max-width: 600px)').matches ? 120 : 210;
document.querySelectorAll('.row').forEach(row => {
  const list = W.filter(w => w.room === row.dataset.room);
  document.querySelector('.ct[data-room="' + row.dataset.room + '"]').textContent = list.length;
  list.forEach((w, k) => {
    const ar = w.tw / w.th, a = document.createElement('a');
    a.className = 'tile'; a.href = '/art/full/' + w.id + '.jpg';
    a.style.flex = ar + ' 1 ' + (ar * H) + 'px'; a.style.aspectRatio = ar;
    a.innerHTML = '<img src="/art/thumb/' + w.id + '.jpg" alt="' + (w.t ? w.t + ' by Deano' : 'Untitled work by Deano') + '" loading="lazy" decoding="async">' + (w.t ? '<span class="t">' + w.t + '</span>' : '');
    a.onclick = e => { e.preventDefault(); viewer.open(k, list); };
    row.appendChild(a);
  });
});
""" + YEAR_JS)


# ---------------------------------------------------------------- /artist/ Artist's Entry (private, code-protected API)
page("/artist/", "Artist's Entry | Deano", """
body { background: #fbfaf7; }
.gate { min-height: 100vh; min-height: 100svh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px 16px; text-align: center; }
.gate .mark { font-size: clamp(60px, 14vw, 120px); }
.gate h1 { font-family: "Archivo Black", sans-serif; font-size: clamp(26px, 5vw, 38px); margin: 26px 0 6px; }
.gate p { margin: 0 0 22px; color: #444; font-size: 18px; }
.pins { display: flex; gap: 14px; margin-bottom: 22px; }
.pins i { width: 22px; height: 22px; border-radius: 50%; border: 3px solid #111; background: #fff; }
.pins i.on { background: #111; }
.pad { display: grid; grid-template-columns: repeat(3, 84px); gap: 12px; }
.pad button { height: 72px; font: 800 28px/1 "Archivo Black", sans-serif; background: #fff; border: 3px solid #111; border-radius: 16px;
  box-shadow: 4px 4px 0 #111; cursor: pointer; }
.pad button:active { transform: translate(2px,2px); box-shadow: 2px 2px 0 #111; }
.pad .dl { font-size: 18px; }
.err { color: #c0281d; font-weight: 600; min-height: 1.5em; margin-top: 16px; }
.studio { display: none; max-width: 1300px; margin: 0 auto; padding: 28px 16px 120px; }
.studio.on { display: block; }
.studio header { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 12px 28px; margin-bottom: 8px; }
.studio header .mark { font-size: 56px; }
.studio h1 { font-family: "Archivo Black", sans-serif; font-size: 30px; margin: 0; }
.studio .how { font-size: 19px; line-height: 1.5; max-width: 760px; margin: 14px 0 18px; }
.bar { position: sticky; top: 0; z-index: 5; background: rgba(251,250,247,.95); backdrop-filter: blur(6px); border-bottom: 3px solid #111;
  padding: 10px 0; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 20px; }
.bar .st { font-weight: 600; margin-left: auto; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 22px; }
.card { background: #fff; border: 3px solid #111; box-shadow: 5px 5px 0 #111; padding: 12px; display: flex; flex-direction: column; gap: 10px; }
.card.changed { box-shadow: 5px 5px 0 var(--green); border-color: var(--green); }
.card .top { display: flex; justify-content: space-between; align-items: center; font-weight: 600; }
.card .num { font-family: "Archivo Black", sans-serif; font-size: 22px; }
.card .ok { font-size: 14px; color: var(--green); }
.box { aspect-ratio: 1; background: #f1efe9; display: grid; place-items: center; overflow: hidden; border: 2px solid #ddd; }
.box img { width: 100%; height: 100%; object-fit: contain; transition: transform .3s; }
.turns { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.turns button { font: 600 17px/1 Archivo, sans-serif; padding: 14px 6px; background: #fff; border: 3px solid #111; border-radius: 12px; cursor: pointer; }
.turns button:hover { background: var(--yellow); }
.card input { font: 16px Archivo, sans-serif; padding: 12px; border: 2px solid #111; border-radius: 10px; width: 100%; }
.done { margin-top: 30px; text-align: center; }
.done button { font: 800 20px/1 "Archivo Black", sans-serif; padding: 18px 30px; background: var(--yellow); border: 3px solid #111; border-radius: 999px; box-shadow: 4px 4px 0 #111; cursor: pointer; }
.thanks { font-size: 20px; font-weight: 600; margin-top: 16px; min-height: 1.5em; }
""", f"""
<section class="gate" id="gate">
  {MARK}
  <h1>Artist&rsquo;s Entry</h1>
  <p>Enter your 4-digit code.</p>
  <div class="pins" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="pad">
    <button>1</button><button>2</button><button>3</button><button>4</button><button>5</button><button>6</button>
    <button>7</button><button>8</button><button>9</button><span></span><button>0</button><button class="dl" aria-label="Delete">&#9003;</button>
  </div>
  <div class="err" id="err" role="alert"></div>
</section>
<section class="studio" id="studio">
  <header>{MARK}<h1>Artist&rsquo;s Entry</h1></header>
  <p class="how">Hi Dean. Turn each piece so it&rsquo;s the right way up, and give it a name if you like. Everything saves by itself. Brett will put your changes on the website.</p>
  <div class="bar"><button class="chip" data-show="all" aria-pressed="true">All pieces</button><button class="chip" data-show="changed" aria-pressed="false">Only my changes</button><span class="st" id="st"></span></div>
  <div class="grid" id="grid"></div>
  <div class="done"><button id="doneBtn">I&rsquo;m done for now</button><div class="thanks" id="thanks"></div></div>
</section>
""", r"""
let pin = '';
try { pin = sessionStorage.getItem('deano-pin') || ''; } catch (e) {}
const dots = document.querySelectorAll('.pins i'), err = document.getElementById('err');
let typed = '';
function paint() { dots.forEach((d, i) => d.classList.toggle('on', i < typed.length)); }
async function api(path, opts = {}) {
  const r = await fetch('/api/artist' + path, { ...opts, headers: { 'content-type': 'application/json', 'x-artist-pin': pin, ...(opts.headers || {}) } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || 'Something went wrong.');
  return j;
}
async function tryLogin() {
  try { await api('/login', { method: 'POST' }); try { sessionStorage.setItem('deano-pin', pin); } catch (e) {} enter(); }
  catch (e) { err.textContent = e.message; typed = ''; pin = ''; paint(); }
}
document.querySelectorAll('.pad button').forEach(b => b.onclick = () => {
  err.textContent = '';
  if (b.classList.contains('dl')) typed = typed.slice(0, -1);
  else if (typed.length < 4) typed += b.textContent;
  paint();
  if (typed.length === 4) { pin = typed; tryLogin(); }
});
document.addEventListener('keydown', e => {
  if (document.getElementById('studio').classList.contains('on')) return;
  if (/^[0-9]$/.test(e.key) && typed.length < 4) { typed += e.key; paint(); if (typed.length === 4) { pin = typed; tryLogin(); } }
  if (e.key === 'Backspace') { typed = typed.slice(0, -1); paint(); }
});

const state = {};
let show = 'all';
const st = document.getElementById('st');
function count() { const n = Object.values(state).filter(s => s.turn || s.title !== s.orig).length; st.textContent = n + (n === 1 ? ' piece changed' : ' pieces changed'); }
const timers = {};
function save(id) {
  clearTimeout(timers[id]);
  timers[id] = setTimeout(async () => {
    const s = state[id], ok = document.querySelector('[data-id="' + id + '"] .ok');
    ok.textContent = 'Saving...';
    try { await api('/edits/' + id, { method: 'PUT', body: JSON.stringify({ turn: s.turn, title: s.title }) }); ok.textContent = 'Saved ✓'; }
    catch (e) { ok.textContent = 'Not saved. ' + e.message; }
  }, 500);
}
function render() {
  const g = document.getElementById('grid'); g.innerHTML = '';
  W.forEach((w, i) => {
    const s = state[w.id], changed = s.turn || s.title !== s.orig;
    if (show === 'changed' && !changed) return;
    const c = document.createElement('div'); c.className = 'card' + (changed ? ' changed' : ''); c.dataset.id = w.id;
    c.innerHTML = '<div class="top"><span class="num">#' + (i + 1) + '</span><span class="ok"></span></div>' +
      '<div class="box"><img src="/art/thumb/' + w.id + '.jpg" alt="Piece ' + (i + 1) + '" loading="lazy" style="transform:rotate(' + s.turn + 'deg)"></div>' +
      '<div class="turns"><button data-d="-90">&#8634; Turn left</button><button data-d="90">Turn right &#8635;</button></div>' +
      '<input type="text" maxlength="120" placeholder="Name this piece (optional)" aria-label="Name for piece ' + (i + 1) + '">';
    c.querySelector('input').value = s.title;
    c.querySelectorAll('.turns button').forEach(b => b.onclick = () => {
      s.turn = ((s.turn + +b.dataset.d) % 360 + 360) % 360;
      c.querySelector('img').style.transform = 'rotate(' + s.turn + 'deg)';
      c.classList.toggle('changed', !!(s.turn || s.title !== s.orig)); count(); save(w.id);
    });
    c.querySelector('input').oninput = e => { s.title = e.target.value; c.classList.toggle('changed', !!(s.turn || s.title !== s.orig)); count(); save(w.id); };
    g.appendChild(c);
  });
}
async function enter() {
  document.getElementById('gate').style.display = 'none';
  document.getElementById('studio').classList.add('on');
  W.forEach(w => state[w.id] = { turn: 0, title: w.t, orig: w.t });
  try { const { edits } = await api('/edits'); edits.forEach(e => { if (state[e.id]) { state[e.id].turn = e.turn; state[e.id].title = e.title || state[e.id].title; } }); } catch (e) {}
  render(); count();
}
document.querySelectorAll('[data-show]').forEach(b => b.onclick = () => {
  show = b.dataset.show; document.querySelectorAll('[data-show]').forEach(x => x.setAttribute('aria-pressed', x === b)); render();
});
document.getElementById('doneBtn').onclick = () => { document.getElementById('thanks').textContent = 'Thank you, Dean. Your changes are saved.'; };
if (pin) tryLogin();
""")

print(f"built /, /one/, /rooms/, /artist/ with {len(works)} works ({REV})")
