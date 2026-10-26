"""Crop a photo of artwork to the paper, and measure its colors. (Rev.7)
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

def _rectish(q, tol=0.06):
    q = order(q)
    t, r, b, l = [np.linalg.norm(q[(i+1) % 4] - q[i]) for i in range(4)]
    return abs(t-b)/max(t, b) < tol and abs(l-r)/max(l, r) < tol

def _angles_ok(q):
    """Every corner between 60 and 120 degrees: a page shot at an angle, not a random blob."""
    q = order(q)
    for i in range(4):
        a, b, c = q[i-1], q[i], q[(i+1) % 4]
        v1, v2 = a - b, c - b
        cos = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)
        if not (60 <= np.degrees(np.arccos(np.clip(cos, -1, 1))) <= 120): return False
    return True

def _search(mask_for, H, W, tol=0.06, edge_ok=False):
    for thr in mask_for:
        for k in (5, 11, 21):
            m = cv2.morphologyEx(thr, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
            n, lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
            cand, ca = None, 0
            for i in range(1, n):
                x, y, bw, bh, ar = stats[i]
                if not edge_ok and (x <= 1 or y <= 1 or x + bw >= W - 1 or y + bh >= H - 1): continue
                if not (x < W/2 < x+bw and y < H/2 < y+bh): continue
                if bw*bh/(W*H) < 0.2: continue
                if ar > ca: cand, ca = i, ar
            if cand is None: continue
            q = _quad_from((lab == cand).astype(np.uint8) * 255)
            if _rectish(q, tol) and _angles_ok(q): return q
    return None

def _white_page(hsv, H, W):
    """Paper that touches the photo edge or sits on a busy surface: find the white page,
    fill in the art, and fit four corners even when the shot is at an angle."""
    v, s = hsv[..., 2].astype(int), hsv[..., 1].astype(int)
    for vt, st in ((165, 50), (145, 60), (185, 40)):
        white = ((v > vt) & (s < st)).astype(np.uint8) * 255
        white = cv2.morphologyEx(white, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(white, connectivity=4)
        if n < 2: continue
        i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        comp = (lab == i).astype(np.uint8) * 255
        # fill the drawing inside the page
        cnts, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filled = np.zeros_like(comp); cv2.drawContours(filled, cnts, -1, 255, -1)
        filled = cv2.morphologyEx(filled, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
        # trim thin bridges to other paper or glare
        filled = cv2.morphologyEx(filled, cv2.MORPH_OPEN, np.ones((41, 41), np.uint8))
        n2, lab2, st2, _ = cv2.connectedComponentsWithStats(filled, connectivity=4)
        if n2 < 2: continue
        j = 1 + int(np.argmax(st2[1:, cv2.CC_STAT_AREA]))
        page = (lab2 == j).astype(np.uint8) * 255
        if page.sum() / 255 < 0.25 * H * W: continue
        q = _quad_from(page)
        if _angles_ok(q) and _rectish(q, 0.3): return q
    return None

def _center_page(hsv, H, W):
    """Page on a darker surface that runs off the photo edge or overlaps other paper:
    take the bright region under the middle of the photo, with heavy cleanup to cut
    thin joins, and fit four corners (angled shots allowed)."""
    v = hsv[..., 2]
    cy, cx = slice(H // 3, 2 * H // 3), slice(W // 3, 2 * W // 3)
    for t in (90, 110, 130):
        for k in (41, 61):
            m = cv2.morphologyEx((v >= t).astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
            n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
            cnt = np.bincount(lab[cy, cx].ravel(), minlength=n); cnt[0] = 0
            c = int(np.argmax(cnt))
            if c == 0: continue
            frac = st[c, cv2.CC_STAT_AREA] / (H * W)
            if not (0.3 <= frac <= 0.95): continue
            q = _quad_from((lab == c).astype(np.uint8) * 255)
            if _angles_ok(q) and _rectish(q, 0.3):
                q[:, 0] = np.clip(q[:, 0], 0, W - 1); q[:, 1] = np.clip(q[:, 1], 0, H - 1)
                return q
    return None

def find_paper(rgb):
    """Return the 4 corners of the paper, or None if no clear paper edge is found."""
    h, w = rgb.shape[:2]
    scale = 1000 / max(h, w)
    small = cv2.resize(rgb, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(small, cv2.COLOR_RGB2HSV)
    H, W = small.shape[:2]
    v, s = hsv[..., 2], hsv[..., 1]
    masks = [((v >= t).astype(np.uint8) * 255) for t in (72, 90, 110, 130, 60, 50)]
    # 1) paper on a dark mat or light box, shot straight on
    q = _search(masks, H, W)
    # 2) same, shot at an angle (keystone)
    if q is None: q = _search(masks, H, W, tol=0.3)
    # 3) page on a dark surface that runs off the photo edge or overlaps other paper
    if q is None: q = _center_page(hsv, H, W)
    # 4) white page on a busy surface
    if q is None: q = _white_page(hsv, H, W)
    return None if q is None else q / scale

def crop_with_quad(im, quad):
    """Warp the four corners (pixels, any order) to a straight rectangle."""
    rgb = np.array(im)
    q = order(np.asarray(quad, dtype=np.float32))
    W = int(max(np.linalg.norm(q[1]-q[0]), np.linalg.norm(q[2]-q[3])))
    H = int(max(np.linalg.norm(q[3]-q[0]), np.linalg.norm(q[2]-q[1])))
    M = cv2.getPerspectiveTransform(q, np.array([[0,0],[W-1,0],[W-1,H-1],[0,H-1]], dtype=np.float32))
    return Image.fromarray(cv2.warpPerspective(rgb, M, (W, H), flags=cv2.INTER_CUBIC))

def crop_to_paper(im, with_quad=False):
    """PIL RGB image in, cropped PIL image out (unchanged if no paper edge found).
    with_quad=True also returns the corners as fractions of the image size (TL, TR, BR, BL)."""
    quad = find_paper(np.array(im))
    if quad is None: return (im, False, None) if with_quad else (im, False)
    q = order(quad)
    out = crop_with_quad(im, q)
    W, H = out.size; inset = int(min(W, H) * 0.006)
    out = out.crop((inset, inset, W - inset, H - inset))
    fr = [[round(float(x) / im.width, 4), round(float(y) / im.height, 4)] for x, y in q]
    return (out, True, fr) if with_quad else (out, True)

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
