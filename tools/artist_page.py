"""Artist's Entry page: CSS, HTML and JS (Rev.6). Imported by build.py."""

CSS = """
body { background: #fbfaf7; }
.gate { min-height: 100vh; min-height: 100svh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px 16px; text-align: center; }
.gate .mark { font-size: clamp(60px, 14vw, 120px); }
.gate h1 { font-family: "Archivo Black", sans-serif; font-size: clamp(26px, 5vw, 38px); margin: 26px 0 6px; }
.gate p { margin: 0 0 22px; color: #444; font-size: 18px; }
.pins { display: flex; gap: 14px; margin-bottom: 22px; }
.pins i { width: 22px; height: 22px; border-radius: 50%; border: 3px solid #111; background: #fff; }
.pins i.on { background: #111; }
.pad { display: grid; grid-template-columns: repeat(3, 84px); gap: 12px; }
.pad button { height: 72px; font: 800 28px/1 "Archivo Black", sans-serif; background: #fff; border: 3px solid #111; border-radius: 16px; box-shadow: 4px 4px 0 #111; cursor: pointer; color: #111; }
.pad button:active { transform: translate(2px,2px); box-shadow: 2px 2px 0 #111; }
.pad .dl { font-size: 18px; }
.err { color: #c0281d; font-weight: 600; min-height: 1.5em; margin-top: 16px; }
.studio { display: none; max-width: 1300px; margin: 0 auto; padding: 24px 16px 120px; }
.studio.on { display: block; }
.studio header { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 12px 28px; }
.studio header .mark { font-size: 52px; }
.studio h1 { font-family: "Archivo Black", sans-serif; font-size: 28px; margin: 0; }
.tabs { display: flex; gap: 8px; margin: 22px 0 0; border-bottom: 3px solid #111; }
.tabs button { font: 700 17px/1 Archivo, sans-serif; padding: 14px 18px; background: #fff; border: 3px solid #111; border-bottom: 0; border-radius: 12px 12px 0 0; cursor: pointer; color: #111; margin-bottom: -3px; }
.tabs button[aria-selected="true"] { background: var(--yellow); }
.how { font-size: 19px; line-height: 1.5; max-width: 780px; margin: 18px 0; }
.bar { position: sticky; top: 0; z-index: 5; background: rgba(251,250,247,.96); backdrop-filter: blur(6px); border-bottom: 3px solid #111;
  padding: 10px 0; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 20px; }
.bar .st { font-weight: 600; }
.pub { margin-left: auto; font: 800 17px/1 "Archivo Black", sans-serif; padding: 14px 20px; background: var(--green); color: #fff; border: 3px solid #111; border-radius: 999px; box-shadow: 3px 3px 0 #111; cursor: pointer; }
.pub:disabled { background: #bbb; cursor: default; }
.msg { width: 100%; font-weight: 600; min-height: 0; }
.msg:empty { display: none; }
.msg.good { color: #13703a; } .msg.bad { color: #c0281d; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 22px; }
.card { background: #fff; border: 3px solid #111; box-shadow: 5px 5px 0 #111; padding: 12px; display: flex; flex-direction: column; gap: 10px; }
.card.changed { box-shadow: 5px 5px 0 var(--green); border-color: var(--green); }
.card.hid .box img { opacity: .35; }
.card .top { display: flex; justify-content: space-between; align-items: center; font-weight: 600; gap: 8px; }
.card .num { font-family: "Archivo Black", sans-serif; font-size: 22px; }
.card .tag { font-size: 13px; background: #111; color: #fff; padding: 4px 8px; border-radius: 999px; display: none; }
.card.hid .tag { display: inline-block; }
.card .ok { font-size: 14px; color: var(--green); }
.box { aspect-ratio: 1; background: #f1efe9; display: grid; place-items: center; overflow: hidden; border: 2px solid #ddd; }
.box img { width: 100%; height: 100%; object-fit: contain; transition: transform .3s, opacity .3s; }
.turns { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.turns button { font: 600 17px/1 Archivo, sans-serif; padding: 14px 6px; background: #fff; border: 3px solid #111; border-radius: 12px; cursor: pointer; color: #111; }
.turns button:hover { background: var(--yellow); }
.card input[type=text] { font: 16px Archivo, sans-serif; padding: 12px; border: 2px solid #111; border-radius: 10px; width: 100%; }
.hide { display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 17px; cursor: pointer; padding: 4px 2px; }
.hide input { width: 26px; height: 26px; accent-color: #111; }
.locked .turns button, .locked input { pointer-events: none; opacity: .5; }
.up { max-width: 780px; }
.pick { display: flex; flex-wrap: wrap; gap: 12px; margin: 10px 0 20px; }
.pick label { font: 800 18px/1 "Archivo Black", sans-serif; padding: 18px 24px; background: var(--yellow); border: 3px solid #111; border-radius: 999px; box-shadow: 4px 4px 0 #111; cursor: pointer; }
.pick input { display: none; }
.tips { background: #fff; border: 3px solid #111; padding: 14px 18px; margin-bottom: 20px; }
.tips b { display: block; margin-bottom: 6px; }
.tips ul { margin: 0; padding-left: 20px; line-height: 1.6; }
.queue { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 14px; }
.qi { background: #fff; border: 3px solid #111; padding: 8px; font-size: 14px; font-weight: 600; }
.qi img { width: 100%; aspect-ratio: 1; object-fit: contain; background: #f1efe9; margin-bottom: 6px; }
.qi.ok { border-color: var(--green); } .qi.bad { border-color: #c0281d; color: #c0281d; }
"""

HTML = """
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
  <div class="tabs" role="tablist">
    <button role="tab" aria-selected="true" data-tab="edit">Turn, name or hide</button>
    <button role="tab" aria-selected="false" data-tab="upload">Add new art</button>
  </div>
  <div id="tab-edit">
    <p class="how">Hi Dean. Turn each piece so it&rsquo;s the right way up, give it a name if you like, and tick <b>Don&rsquo;t show</b> on any piece you want off the website. Everything saves by itself. Press <b>Publish to website</b> when you&rsquo;re ready.</p>
    <div class="bar">
      <button class="chip" data-show="all" aria-pressed="true">All pieces</button>
      <button class="chip" data-show="changed" aria-pressed="false">Only my changes</button>
      <button class="chip" data-show="hidden" aria-pressed="false">Hidden</button>
      <span class="st" id="st"></span>
      <button class="pub" id="pub">Publish to website</button>
      <div class="msg" id="msg" role="status"></div>
    </div>
    <div class="grid" id="grid"></div>
  </div>
  <div id="tab-upload" class="up" hidden>
    <p class="how">Add photos of new art. Each photo is straightened and cropped to the paper, then shows up at the top of the gallery in about 3 minutes. After that, come back to the first tab to turn it and give it a name.</p>
    <div class="tips"><b>For the best photo</b><ul>
      <li>Lay the art flat on a dark table or the black board.</li>
      <li>Hold the phone straight above it so the whole page fits with a little dark border around it.</li>
      <li>Use daylight or a bright room, and keep your shadow off the paper.</li>
    </ul></div>
    <div class="pick">
      <label>Take a photo<input type="file" accept="image/*" capture="environment" id="cam"></label>
      <label>Choose photos<input type="file" accept="image/*,.heic,.heif" multiple id="files"></label>
    </div>
    <div class="msg" id="umsg" role="status"></div>
    <div class="queue" id="queue"></div>
  </div>
</section>
"""

JS = r"""
let pin = '';
try { pin = sessionStorage.getItem('deano-pin') || ''; } catch (e) {}
const dots = document.querySelectorAll('.pins i'), err = document.getElementById('err');
let typed = '', canPublish = false;
function paint() { dots.forEach((d, i) => d.classList.toggle('on', i < typed.length)); }
async function api(path, opts = {}) {
  const r = await fetch('/api/artist' + path, { ...opts, headers: { 'content-type': 'application/json', 'x-artist-pin': pin, ...(opts.headers || {}) } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || 'Something went wrong.');
  return j;
}
async function tryLogin() {
  try { const j = await api('/login', { method: 'POST' }); canPublish = !!j.canPublish; try { sessionStorage.setItem('deano-pin', pin); } catch (e) {} enter(); }
  catch (e) { err.textContent = e.message; typed = ''; pin = ''; paint(); try { sessionStorage.removeItem('deano-pin'); } catch (x) {} }
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

// ---- tabs
document.querySelectorAll('[data-tab]').forEach(b => b.onclick = () => {
  document.querySelectorAll('[data-tab]').forEach(x => x.setAttribute('aria-selected', x === b));
  document.getElementById('tab-edit').hidden = b.dataset.tab !== 'edit';
  document.getElementById('tab-upload').hidden = b.dataset.tab !== 'upload';
});

// ---- turn, name, hide
const state = {};
let show = 'all', locked = false;
const st = document.getElementById('st'), msg = document.getElementById('msg'), pub = document.getElementById('pub');
const isChanged = s => !!(s.turn || s.title !== s.orig || s.hidden !== s.origHidden);
function count() {
  const n = Object.values(state).filter(isChanged).length;
  st.textContent = n + (n === 1 ? ' change' : ' changes') + ' saved';
  pub.disabled = locked || !n || !canPublish;
}
const timers = {};
function save(id) {
  clearTimeout(timers[id]);
  timers[id] = setTimeout(async () => {
    const s = state[id], ok = document.querySelector('[data-id="' + id + '"] .ok');
    if (ok) ok.textContent = 'Saving...';
    try { await api('/edits/' + id, { method: 'PUT', body: JSON.stringify({ turn: s.turn, title: s.title, hidden: s.hidden }) }); if (ok) ok.textContent = 'Saved ✓'; }
    catch (e) { if (ok) ok.textContent = 'Not saved. ' + e.message; }
  }, 500);
}
function render() {
  const g = document.getElementById('grid'); g.innerHTML = '';
  W.forEach((w, i) => {
    const s = state[w.id];
    if (show === 'changed' && !isChanged(s)) return;
    if (show === 'hidden' && !s.hidden) return;
    const c = document.createElement('div'); c.className = 'card'; c.dataset.id = w.id;
    c.innerHTML = '<div class="top"><span class="num">#' + (i + 1) + '</span><span class="tag">Hidden</span><span class="ok"></span></div>' +
      '<div class="box"><img src="/art/thumb/' + w.id + '.jpg" alt="Piece ' + (i + 1) + '" loading="lazy"></div>' +
      '<div class="turns"><button data-d="-90">&#8634; Turn left</button><button data-d="90">Turn right &#8635;</button></div>' +
      '<input type="text" maxlength="120" placeholder="Name this piece (optional)" aria-label="Name for piece ' + (i + 1) + '">' +
      '<label class="hide"><input type="checkbox"> Don&rsquo;t show on website</label>';
    const img = c.querySelector('.box img'), inp = c.querySelector('input[type=text]'), cb = c.querySelector('input[type=checkbox]');
    const refresh = () => { img.style.transform = 'rotate(' + s.turn + 'deg)'; c.classList.toggle('changed', isChanged(s)); c.classList.toggle('hid', s.hidden); count(); };
    inp.value = s.title; cb.checked = s.hidden;
    c.querySelectorAll('.turns button').forEach(b => b.onclick = () => { s.turn = ((s.turn + +b.dataset.d) % 360 + 360) % 360; refresh(); save(w.id); });
    inp.oninput = () => { s.title = inp.value; refresh(); save(w.id); };
    cb.onchange = () => { s.hidden = cb.checked; refresh(); save(w.id); };
    refresh();
    g.appendChild(c);
  });
  document.getElementById('studio').classList.toggle('locked', locked);
}
async function enter() {
  document.getElementById('gate').style.display = 'none';
  document.getElementById('studio').classList.add('on');
  W.forEach(w => state[w.id] = { turn: 0, title: w.t, orig: w.t, hidden: !!w.x, origHidden: !!w.x });
  try {
    const { edits } = await api('/edits');
    edits.forEach(e => { const s = state[e.id]; if (s) { s.turn = e.turn; s.title = e.title ?? s.title; s.hidden = !!e.hidden; } });
  } catch (e) {}
  if (!canPublish) { pub.style.display = 'none'; msg.className = 'msg'; msg.textContent = 'Your changes are saved. Brett will put them on the website.'; }
  render(); count();
}
document.querySelectorAll('[data-show]').forEach(b => b.onclick = () => {
  show = b.dataset.show; document.querySelectorAll('[data-show]').forEach(x => x.setAttribute('aria-pressed', x === b)); render();
});
pub.onclick = async () => {
  pub.disabled = true; msg.className = 'msg'; msg.textContent = 'Publishing...';
  try {
    const j = await api('/publish', { method: 'POST' });
    locked = true; render(); count();
    msg.className = 'msg good';
    msg.textContent = 'Sent! Your ' + j.count + (j.count === 1 ? ' change' : ' changes') + ' will be on the website in about 3 minutes. Reload this page after that before making more changes.';
  } catch (e) { msg.className = 'msg bad'; msg.textContent = e.message; pub.disabled = false; }
};

// ---- upload
const queue = document.getElementById('queue'), umsg = document.getElementById('umsg');
const toB64 = blob => new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(String(r.result).split(',')[1]); r.onerror = rej; r.readAsDataURL(blob); });
async function shrink(file) {
  // Re-encode to JPEG, max 3000 px, with the phone's orientation applied. Falls back to the original file.
  try {
    const bmp = await createImageBitmap(file, { imageOrientation: 'from-image' });
    const k = Math.min(1, 3000 / Math.max(bmp.width, bmp.height));
    const cv = document.createElement('canvas'); cv.width = Math.round(bmp.width * k); cv.height = Math.round(bmp.height * k);
    cv.getContext('2d').drawImage(bmp, 0, 0, cv.width, cv.height);
    const blob = await new Promise(r => cv.toBlob(r, 'image/jpeg', 0.9));
    if (blob) return { blob, ext: 'jpg', preview: URL.createObjectURL(blob) };
  } catch (e) {}
  const ext = (file.name.split('.').pop() || 'jpg').toLowerCase();
  return { blob: file, ext, preview: '' };
}
async function upload(files) {
  if (!canPublish) { umsg.className = 'msg bad'; umsg.textContent = 'Uploading is not set up yet. Ask Brett.'; return; }
  let done = 0;
  for (const f of files) {
    const q = document.createElement('div'); q.className = 'qi'; q.innerHTML = '<img alt=""><div>Getting ready...</div>';
    queue.prepend(q); const lbl = q.querySelector('div');
    try {
      const { blob, ext, preview } = await shrink(f);
      if (preview) q.querySelector('img').src = preview;
      if (blob.size > 15 * 1024 * 1024) throw new Error('Too large');
      lbl.textContent = 'Uploading...';
      await api('/upload', { method: 'POST', body: await toB64(blob), headers: { 'content-type': 'text/plain', 'x-file-ext': ext } });
      q.classList.add('ok'); lbl.textContent = 'Uploaded ✓'; done++;
    } catch (e) { q.classList.add('bad'); lbl.textContent = 'Not uploaded. ' + e.message; }
  }
  if (done) { umsg.className = 'msg good'; umsg.textContent = done + (done === 1 ? ' photo' : ' photos') + ' sent. New art shows at the top of the gallery in about 3 minutes.'; }
}
document.getElementById('files').onchange = e => { upload([...e.target.files]); e.target.value = ''; };
document.getElementById('cam').onchange = e => { upload([...e.target.files]); e.target.value = ''; };

if (pin) tryLogin();
"""
