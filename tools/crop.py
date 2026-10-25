"""Crop a photo of artwork to the paper, and measure its colors. (Rev.6)
Used by tools/apply.py inside the GitHub Action."""
import numpy as np, cv2
from PIL import Image

def order(pts):
    s = pts.sum(1); d = np.diff(pts, axis=1).ravel()
    return np.array([pts[np.argmin(s)], pts[np.argmin(d)], pts[np.argmax(s)], pts[np.argmax(d)]], dtype=np.float32)

def _quad_from(comp):
    cnts, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    hull = cv2.convexHull(c); peri = cv2.arcLength(hull, True)
    for eps in (0.01, 0.02, 0.03, 0.05):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4: return ap.reshape(4, 2).astype(np.float32)
    return cv2.boxPoints(cv2.minAreaRect(hull)).astype(np.float32)

def _rectish(q):
    q = order(q)
    t, r, b, l = [np.linalg.norm(q[(i+1) % 4] - q[i]) for i in range(4)]
    return abs(t-b)/max(t, b) < 0.06 and abs(l-r)/max(l, r) < 0.06

def _search(mask_for, H, W):
    for thr in mask_for:
        for k in (5, 11, 21):
            m = cv2.morphologyEx(thr, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
            n, lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
            cand, ca = None, 0
            for i in range(1, n):
                x, y, bw, bh, ar = stats[i]
                if x <= 1 or y <= 1 or x + bw >= W - 1 or y + bh >= H - 1: continue
                if not (x < W/2 < x+bw and y < H/2 < y+bh): continue
                if bw*bh/(W*H) < 0.2: continue
                if ar > ca: cand, ca = i, ar
            if cand is None: continue
            q = _quad_from((lab == cand).astype(np.uint8) * 255)
            if _rectish(q): return q
    return None

def find_paper(rgb):
    """Return the 4 corners of the paper, or None if no clear paper edge is found."""
    h, w = rgb.shape[:2]
    scale = 1000 / max(h, w)
    small = cv2.resize(rgb, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(small, cv2.COLOR_RGB2HSV)
    H, W = small.shape[:2]
    v, s = hsv[..., 2], hsv[..., 1]
    # 1) paper on a dark mat or table: everything brighter than the background
    masks = [((v >= t).astype(np.uint8) * 255) for t in (72, 90, 110, 130, 60, 50)]
    q = _search(masks, H, W)
    if q is None:
        # 2) white paper on a lighter surface: bright, low-saturation pixels with holes filled
        white = ((v > 185) & (s < 45)).astype(np.uint8) * 255
        white = cv2.morphologyEx(white, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
        q = _search([white], H, W)
    return None if q is None else q / scale

def crop_to_paper(im):
    """PIL RGB image in, cropped PIL image out (unchanged if no paper edge found)."""
    rgb = np.array(im)
    quad = find_paper(rgb)
    if quad is None: return im, False
    q = order(quad)
    W = int(max(np.linalg.norm(q[1]-q[0]), np.linalg.norm(q[2]-q[3])))
    H = int(max(np.linalg.norm(q[3]-q[0]), np.linalg.norm(q[2]-q[1])))
    M = cv2.getPerspectiveTransform(q, np.array([[0,0],[W-1,0],[W-1,H-1],[0,H-1]], dtype=np.float32))
    warp = cv2.warpPerspective(rgb, M, (W, H), flags=cv2.INTER_CUBIC)
    inset = int(min(W, H) * 0.006)
    return Image.fromarray(warp[inset:H-inset, inset:W-inset]), True

def colors(im):
    """Palette, color groups and simple stats from a small copy of the image."""
    t = im.copy(); t.thumbnail((640, 640))
    a = np.array(t.convert("RGB")); hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV).reshape(-1, 3).astype(int)
    paper = float(((hsv[:, 2] > 185) & (hsv[:, 1] < 40)).mean())
    sel = (hsv[:, 1] > 70) & (hsv[:, 2] > 70)
    colorful = float(sel.mean())
    def bucket(h):
        for nm, lo, hi in [('red',0,8),('orange',8,20),('yellow',20,35),('green',35,80),('blue',80,130),('purple',130,155),('pink',155,172),('red',172,181)]:
            if lo <= h < hi: return nm
    counts = {}
    for h in hsv[sel][:, 0]:
        b = bucket(h); counts[b] = counts.get(b, 0) + 1
    tot = sum(counts.values()) or 1
    hues = {k: round(v / tot, 3) for k, v in sorted(counts.items(), key=lambda x: -x[1])}
    px = a.reshape(-1, 3)[sel].astype(np.float32)
    if len(px) > 50:
        _, lab, cent = cv2.kmeans(px, 4, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1), 2, cv2.KMEANS_PP_CENTERS)
        idx = np.argsort(-np.bincount(lab.ravel(), minlength=4))
        pal = ['#%02x%02x%02x' % tuple(int(c) for c in cent[i]) for i in idx]
    else:
        pal = ['#888888']
    m = {'red':'red','pink':'red','orange':'warm','yellow':'warm','blue':'blue','purple':'blue','green':'green'}
    if colorful < 0.05: groups = ['bw']
    else:
        out = {}
        for h, s in hues.items(): out[m[h]] = out.get(m[h], 0) + s
        srt = sorted(out.items(), key=lambda x: -x[1])
        groups = [srt[0][0]] + [k for k, v in srt[1:] if v >= 0.3]
    room = 'paint' if (paper < 0.3 and colorful > 0.3) else 'shapes'
    return {"paper": round(paper, 3), "colorful": round(colorful, 3), "hues": hues, "palette": pal, "colors": groups, "room": room}
