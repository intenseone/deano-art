// Deano full-screen viewer (Rev.2). Usage: const v = DeanoViewer(list); v.open(index)
// list items: {id, t}
window.DeanoViewer = function (list) {
  let lb = document.querySelector('.dv');
  if (!lb) {
    lb = document.createElement('div');
    lb.className = 'dv';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Artwork viewer');
    lb.innerHTML = '<button class="dv-x" aria-label="Close">&times;</button>' +
      '<button class="dv-prev" aria-label="Previous">&#8592;</button>' +
      '<img alt=""><div class="dv-cap"></div>' +
      '<button class="dv-next" aria-label="Next">&#8594;</button>';
    document.body.appendChild(lb);
  }
  const im = lb.querySelector('img'), cap = lb.querySelector('.dv-cap');
  let cur = 0, last = null, items = list;
  const n = () => items.length;
  function show(i) {
    cur = (i + n()) % n();
    const w = items[cur];
    im.src = '/art/full/' + w.id + '.jpg';
    im.alt = w.t ? w.t + ' by Deano' : 'Untitled work by Deano';
    cap.textContent = (w.t ? w.t + '  ·  ' : '') + (cur + 1) + ' of ' + n();
    [cur + 1, cur - 1].forEach(j => { const p = new Image(); p.src = '/art/full/' + items[(j + n()) % n()].id + '.jpg'; });
  }
  function open(i, newList) {
    if (newList) items = newList;
    last = document.activeElement; show(i);
    lb.classList.add('on'); document.body.style.overflow = 'hidden';
    lb.querySelector('.dv-x').focus();
  }
  function close() { lb.classList.remove('on'); document.body.style.overflow = ''; if (last) last.focus(); }
  lb.querySelector('.dv-x').onclick = close;
  lb.querySelector('.dv-prev').onclick = () => show(cur - 1);
  lb.querySelector('.dv-next').onclick = () => show(cur + 1);
  lb.onclick = e => { if (e.target === lb) close(); };
  document.addEventListener('keydown', e => {
    if (!lb.classList.contains('on')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show(cur + 1);
    if (e.key === 'ArrowLeft') show(cur - 1);
  });
  let sx = null;
  lb.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', e => {
    if (sx === null) return;
    const dx = e.changedTouches[0].clientX - sx;
    if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
    sx = null;
  });
  return { open };
};
