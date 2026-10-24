"""Build the 4 layout previews under public/preview/. Run: python3 build_previews.py
Reads works.json (id, title, sizes, palette, room, colors)."""
import json, os

REV = "Rev.2"
works = json.load(open("works.json"))
DATA = json.dumps([{
    "id": w["id"], "t": w.get("title") or "", "w": w["w"], "h": w["h"], "tw": w["tw"], "th": w["th"],
    "p": w["palette"][:3], "room": w["room"], "c": w["colors"], "f": w["colorful"],
} for w in works], separators=(",", ":"))

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>__TITLE__ | Deano preview</title>
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
PAGES = [("wall", "Gallery wall"), ("one", "One at a time"), ("rooms", "Rooms"), ("featured", "Featured")]

def bar(cur):
    links = ['<a href="/">Current site</a>', f'<a href="/preview/"{" aria-current=\"page\"" if cur == "index" else ""}>All</a>']
    for slug, name in PAGES:
        links.append(f'<a href="/preview/{slug}/"{" aria-current=\"page\"" if cur == slug else ""}>{name}</a>')
    return '<nav class="pv-bar" aria-label="Layout previews">' + "".join(links) + "</nav>"

def page(slug, title, css, body, js):
    out = HEAD.replace("__TITLE__", title).replace("__CSS__", css) + body + bar(slug)
    out += '\n<script src="/assets/viewer.js"></script>\n<script>\nconst W = ' + DATA + ';\n' + js + '\n</script>\n'
    out += f'<!-- {REV} -->\n</body>\n</html>\n'
    d = "public/preview" + ("" if slug == "index" else f"/{slug}")
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(out)

# ---------------------------------------------------------------- 1. Gallery wall
page("wall", "Gallery wall", """
body { --wall: #24344d; background: var(--wall); transition: background .5s; min-height: 100vh;
  background-image: radial-gradient(ellipse at 50% -10%, rgba(255,255,255,.14), transparent 60%); color: #f6f1e7; }
header { max-width: 1300px; margin: 0 auto; padding: 40px 20px 10px; display: flex; flex-wrap: wrap; align-items: flex-end; gap: 18px 32px; }
header .mark { font-size: clamp(56px, 10vw, 120px); color: #f6f1e7; }
header .mark .dots i { border-color: #f6f1e7; }
.tools { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-left: auto; }
.tools .lbl { font-weight: 600; font-size: 14px; opacity: .8; margin-right: 2px; }
.sw-btn { width: 34px; height: 34px; border-radius: 50%; border: 3px solid #f6f1e7; cursor: pointer; padding: 0; }
.sw-btn[aria-pressed="true"] { outline: 3px solid var(--yellow); outline-offset: 2px; }
.wall { max-width: 1400px; margin: 0 auto; padding: 40px 20px 120px; display: flex; flex-wrap: wrap;
  justify-content: center; align-items: center; gap: clamp(22px, 4vw, 54px); }
.fr { --r: 0deg; width: var(--sz); transform: rotate(var(--r)); transition: transform .25s, box-shadow .25s;
  background: #fff; padding: calc(var(--sz) * .06); border: clamp(6px, 1vw, 11px) solid #111;
  box-shadow: 0 18px 30px rgba(0,0,0,.45), 0 3px 6px rgba(0,0,0,.3); cursor: zoom-in; display: block; }
.fr:hover, .fr:focus-visible { transform: rotate(0deg) scale(1.04); box-shadow: 0 26px 44px rgba(0,0,0,.55); outline: none; z-index: 2; position: relative; }
.fr img { width: 100%; height: auto; }
.fr.s { --sz: clamp(130px, 17vw, 220px); } .fr.m { --sz: clamp(150px, 23vw, 300px); } .fr.l { --sz: clamp(170px, 31vw, 420px); }
.plate { display: block; margin-top: 8px; font: 600 12px/1.2 Archivo, sans-serif; color: #111; text-align: center; letter-spacing: .02em; }
@media (max-width: 600px) { .fr.s, .fr.m, .fr.l { --sz: 40vw; } .wall { gap: 26px 18px; } .tools { margin-left: 0; } }
""", f"""
<header>
  {MARK}
  <div class="tools">
    <span class="lbl">Wall</span>
    <button class="sw-btn" data-wall="#24344d" style="background:#24344d" aria-label="Deep blue wall" aria-pressed="true"></button>
    <button class="sw-btn" data-wall="#2b2b2b" style="background:#2b2b2b" aria-label="Charcoal wall"></button>
    <button class="sw-btn" data-wall="#8c2f2a" style="background:#8c2f2a" aria-label="Red wall"></button>
    <button class="sw-btn" data-wall="#e9e2d3" style="background:#e9e2d3" aria-label="Cream wall"></button>
    <button class="chip" id="shuffle">Shuffle the wall</button>
  </div>
</header>
<main class="wall" id="wall"></main>
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
document.querySelectorAll('.sw-btn').forEach(b => b.onclick = () => {
  document.body.style.setProperty('--wall', b.dataset.wall);
  const light = b.dataset.wall === '#e9e2d3';
  document.body.style.color = light ? '#111' : '#f6f1e7';
  document.querySelector('header .mark').style.color = light ? '#111' : '#f6f1e7';
  document.querySelectorAll('header .mark .dots i').forEach(i => i.style.borderColor = light ? '#111' : '#f6f1e7');
  document.querySelectorAll('.sw-btn').forEach(x => x.setAttribute('aria-pressed', x === b));
});
""")

# ---------------------------------------------------------------- 2. One at a time
page("one", "One at a time", """
html { scroll-snap-type: y mandatory; }
body { transition: background-color .7s ease; }
.slide { height: 100vh; height: 100svh; scroll-snap-align: start; display: flex; flex-direction: column;
  align-items: center; justify-content: center; padding: 24px 16px 84px; position: relative; }
.intro .mark { font-size: clamp(72px, 16vw, 200px); }
.intro p { font-size: clamp(18px, 2.4vw, 24px); margin: 22px 0 0; text-align: center; }
.intro .hint { margin-top: 40px; font-weight: 600; animation: bob 1.6s ease-in-out infinite; }
@keyframes bob { 50% { transform: translateY(8px); } }
.slide figure { margin: 0; display: flex; flex-direction: column; align-items: center; max-width: 100%; }
.slide img { max-height: calc(100svh - 170px); max-width: min(92vw, 1300px); width: auto; height: auto; background: #fff;
  border: 4px solid #111; box-shadow: 10px 10px 0 #111; cursor: zoom-in; }
.slide figcaption { margin-top: 22px; font-weight: 600; font-size: 17px; text-align: center; }
.slide figcaption .n { opacity: .6; font-weight: 400; margin-left: 8px; }
.progress { position: fixed; top: 0; left: 0; height: 6px; background: #111; width: 0; z-index: 10; transition: width .3s; }
.top { position: fixed; top: 16px; left: 18px; z-index: 10; font-size: 34px; }
@media (max-width: 600px) { .slide img { box-shadow: 6px 6px 0 #111; border-width: 3px; max-height: calc(100svh - 190px); } .top { font-size: 26px; } }
""", f"""
<div class="progress" id="prog"></div>
<div class="top">{MARK}</div>
<section class="slide intro" data-bg="#fbfaf7">
  <span class="mark" style="font-size:clamp(72px,16vw,200px)">Deano<span class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i></span></span>
  <p>Drawings and paintings by Dean Greenberg.</p>
  <div class="hint">Scroll to walk through all <span id="cnt"></span> pieces &darr;</div>
</section>
<main id="slides"></main>
""", """
const box = document.getElementById('slides'); const viewer = DeanoViewer(W);
document.getElementById('cnt').textContent = W.length;
document.querySelector('.top').style.opacity = 0;
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
  document.querySelector('.top').style.opacity = i === undefined ? 0 : 1;
  document.getElementById('prog').style.width = i === undefined ? 0 : ((+i + 1) / W.length * 100) + '%';
}), { threshold: .55 });
document.querySelectorAll('.slide').forEach(s => io.observe(s));
document.addEventListener('keydown', e => {
  if (document.querySelector('.dv.on')) return;
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); scrollBy({ top: innerHeight, behavior: 'smooth' }); }
  if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); scrollBy({ top: -innerHeight, behavior: 'smooth' }); }
});
""")

# ---------------------------------------------------------------- 3. Rooms
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
page("rooms", "Rooms", """
header { max-width: 1400px; margin: 0 auto; padding: 44px 20px 8px; }
header .mark { font-size: clamp(60px, 12vw, 140px); }
header p { font-size: clamp(17px, 2.2vw, 21px); margin: 16px 0 0; }
.rnav { position: sticky; top: 0; z-index: 5; background: rgba(251,250,247,.94); backdrop-filter: blur(6px);
  border-bottom: 3px solid #111; }
.rnav div { max-width: 1400px; margin: 0 auto; padding: 12px 20px; display: flex; gap: 10px; overflow-x: auto; }
.rnav .ct { opacity: .6; font-weight: 400; }
.room { max-width: 1400px; margin: 0 auto; padding: 46px 20px 10px; scroll-margin-top: 70px; }
.band { display: flex; height: 16px; border: 3px solid #111; width: min(320px, 70%); margin-bottom: 18px; }
.band i { flex: 1; } .band i + i { border-left: 3px solid #111; }
.room h2 { font-family: "Archivo Black", sans-serif; font-size: clamp(30px, 5vw, 52px); line-height: 1; margin: 0; }
.desc { margin: 10px 0 24px; color: #444; }
.row { display: flex; flex-wrap: wrap; gap: 16px; }
.row::after { content: ""; flex-grow: 999; }
.tile { display: block; position: relative; background: #fff; border: 3px solid #111; overflow: hidden; cursor: zoom-in; }
.tile img { width: 100%; height: 100%; object-fit: cover; }
.tile:hover { box-shadow: 6px 6px 0 #111; transform: translate(-2px,-2px); }
.tile { transition: transform .12s, box-shadow .12s; }
.tile .t { position: absolute; left: 0; bottom: 0; background: #111; color: #fff; font: 600 12px/1 Archivo, sans-serif; padding: 6px 8px; }
footer { height: 110px; }
@media (max-width: 600px) { .row { gap: 10px; } .tile { border-width: 2px; } }
""", f"""
<header>{MARK}<p>Drawings and paintings by Dean Greenberg, grouped by how they were made.</p></header>
<nav class="rnav" aria-label="Rooms"><div>{room_nav}</div></nav>
{room_secs}
<footer></footer>
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
""")

# ---------------------------------------------------------------- 4. Featured + color filter
FILTERS = [("all", "All", None), ("red", "Red", "#e2382b"), ("warm", "Yellow and orange", "#f5c518"),
           ("blue", "Blue", "#1f5fd6"), ("green", "Green", "#1e9e57"), ("bw", "Black and white", "#ffffff")]
chips = "".join(
    f'<button class="chip" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">' +
    (f'<span class="sw" style="background:{c}"></span>' if c else "") + f'{n}</button>' for k, n, c in FILTERS)
page("featured", "Featured", """
.hero { max-width: 1400px; margin: 0 auto; padding: 36px 20px 30px; display: grid; grid-template-columns: 1.5fr 1fr; gap: 40px; align-items: center; }
.hero .art { background: #fff; border: 5px solid #111; box-shadow: 14px 14px 0 var(--accent, #111); transition: box-shadow .4s; cursor: zoom-in; display: block; }
.hero .art img { width: 100%; height: auto; transition: opacity .3s; }
.side .mark { font-size: clamp(64px, 9vw, 130px); }
.side p { font-size: clamp(17px, 2vw, 21px); margin: 18px 0 0; }
.now { margin-top: 30px; padding-top: 18px; border-top: 3px solid #111; }
.now .k { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; color: #555; }
.now .t { font-family: "Archivo Black", sans-serif; font-size: clamp(24px, 3vw, 34px); line-height: 1.1; margin: 6px 0 16px; }
.now .btns { display: flex; gap: 10px; flex-wrap: wrap; }
.filters { max-width: 1400px; margin: 0 auto; padding: 22px 20px 6px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
  border-top: 3px solid #111; }
.filters .ct { margin-left: auto; font-weight: 600; color: #555; }
main { max-width: 1400px; margin: 0 auto; padding: 18px 20px 120px; }
.grid { columns: 4 240px; column-gap: 20px; }
.card { break-inside: avoid; margin: 0 0 20px; display: block; background: #fff; border: 3px solid #111; box-shadow: 5px 5px 0 #111;
  transition: transform .12s, box-shadow .12s; cursor: zoom-in; }
.card:hover { transform: translate(-2px,-2px); box-shadow: 7px 7px 0 #111; }
.card img { width: 100%; height: auto; }
.card[hidden] { display: none; }
@media (max-width: 800px) { .hero { grid-template-columns: 1fr; gap: 24px; } .side { order: -1; } .now { margin-top: 18px; } }
@media (max-width: 600px) { .grid { columns: 2 140px; column-gap: 12px; } .card { margin-bottom: 12px; border-width: 2px; box-shadow: 3px 3px 0 #111; }
  .hero .art { box-shadow: 8px 8px 0 var(--accent, #111); border-width: 3px; } .filters .ct { margin-left: 0; width: 100%; } }
""", f"""
<section class="hero">
  <a class="art" id="feat" href="#"><img id="featImg" alt=""></a>
  <div class="side">
    {MARK}
    <p>Drawings and paintings by Dean Greenberg.</p>
    <div class="now">
      <div class="k">Featured piece</div>
      <div class="t" id="featT"></div>
      <div class="btns"><button class="chip" id="another">Show another</button><button class="chip" id="full">View full size</button></div>
    </div>
  </div>
</section>
<div class="filters" role="group" aria-label="Filter by color">{chips}<button class="chip" id="shuf">Shuffle</button><span class="ct" id="ct"></span></div>
<main><div class="grid" id="grid"></div></main>
""", """
const grid = document.getElementById('grid'); const viewer = DeanoViewer(W);
const pool = W.map((w, i) => i).filter(i => W[i].t || W[i].f > .42);
let fi = pool[Math.floor(Math.random() * pool.length)], view = W.slice(), filter = 'all';
function feature(i) {
  fi = i; const w = W[i], img = document.getElementById('featImg');
  img.style.opacity = 0;
  img.onload = () => img.style.opacity = 1;
  img.src = '/art/full/' + w.id + '.jpg'; img.alt = (w.t || 'Untitled work') + ' by Deano';
  document.getElementById('featT').textContent = w.t || 'Untitled, no. ' + (i + 1);
  document.querySelector('.hero .art').style.setProperty('--accent', w.p[0] || '#111');
}
feature(fi);
document.getElementById('another').onclick = () => { let n; do { n = pool[Math.floor(Math.random() * pool.length)]; } while (n === fi && pool.length > 1); feature(n); };
document.getElementById('full').onclick = () => viewer.open(fi, W);
document.getElementById('feat').onclick = e => { e.preventDefault(); viewer.open(fi, W); };
function render() {
  grid.innerHTML = '';
  const list = view.filter(w => filter === 'all' || w.c.includes(filter));
  document.getElementById('ct').textContent = list.length + (list.length === 1 ? ' piece' : ' pieces');
  list.forEach((w, k) => {
    const a = document.createElement('a'); a.className = 'card'; a.href = '/art/full/' + w.id + '.jpg';
    a.innerHTML = '<img src="/art/thumb/' + w.id + '.jpg" width="' + w.tw + '" height="' + w.th + '" alt="' + (w.t ? w.t + ' by Deano' : 'Untitled work by Deano') + '" loading="lazy" decoding="async">';
    a.onclick = e => { e.preventDefault(); viewer.open(k, list); };
    grid.appendChild(a);
  });
}
render();
document.querySelectorAll('[data-f]').forEach(b => b.onclick = () => {
  filter = b.dataset.f;
  document.querySelectorAll('[data-f]').forEach(x => x.setAttribute('aria-pressed', x === b));
  render();
});
document.getElementById('shuf').onclick = () => {
  for (let i = view.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [view[i], view[j]] = [view[j], view[i]]; }
  render();
};
""")

# ---------------------------------------------------------------- preview index
pick = {"wall": "9294", "one": "9367", "rooms": "9310", "featured": "9349"}
desc = {
    "wall": "Pieces hung on a colored wall at mixed sizes and slight tilts. Change the wall color or shuffle the hang.",
    "one": "Each piece fills the screen. The background takes on that piece's colors as you scroll.",
    "rooms": "Pieces grouped into Bold Shapes, Paint, Lines and Scribbles, and People and Places.",
    "featured": "One large piece up top that changes each visit, with color filters and shuffle below.",
}
cards = "".join(
    f'<a class="pc" href="/preview/{s}/"><img src="/art/thumb/{pick[s]}.jpg" alt="" loading="lazy"><span class="n">{i+1}</span>'
    f'<h2>{n}</h2><p>{desc[s]}</p><span class="go">Open preview &rarr;</span></a>'
    for i, (s, n) in enumerate(PAGES))
page("index", "Layout previews", """
header { max-width: 1200px; margin: 0 auto; padding: 44px 20px 10px; }
header .mark { font-size: clamp(56px, 10vw, 110px); }
header h1 { font-family: "Archivo Black", sans-serif; font-size: clamp(26px, 4vw, 40px); margin: 26px 0 6px; }
header p { margin: 0; color: #444; }
.cards { max-width: 1200px; margin: 0 auto; padding: 26px 20px 130px; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 24px; }
.pc { display: block; text-decoration: none; background: #fff; border: 3px solid #111; box-shadow: 6px 6px 0 #111; position: relative; transition: transform .12s, box-shadow .12s; }
.pc:hover { transform: translate(-2px,-2px); box-shadow: 9px 9px 0 #111; }
.pc img { width: 100%; aspect-ratio: 4/3; object-fit: cover; border-bottom: 3px solid #111; }
.pc .n { position: absolute; top: 10px; left: 10px; background: var(--yellow); border: 3px solid #111; border-radius: 50%; width: 38px; height: 38px;
  display: grid; place-items: center; font: 800 17px/1 "Archivo Black", sans-serif; }
.pc h2 { font-family: "Archivo Black", sans-serif; font-size: 24px; margin: 14px 16px 4px; }
.pc p { margin: 0 16px; color: #333; }
.pc .go { display: inline-block; margin: 12px 16px 16px; font-weight: 600; border-bottom: 3px solid var(--yellow); }
""", f"""
<header>{MARK}<h1>Layout previews</h1><p>Four ways to show the work. The live home page stays the same until you pick one.</p></header>
<main class="cards">{cards}</main>
""", "")

print(f"previews built ({REV})")
