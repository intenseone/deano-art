"""Apply uploads and published edits, then rebuild. Run by .github/workflows/apply.yml (Rev.6).

inbox/*                 new photos from Artist's Entry -> cropped, sized, added to the top of the gallery
edits/pending-*.json    [{id, turn, title, hidden}] from the Publish button -> applied to images and works.json
"""
import json, os, glob, shutil, subprocess, sys
from PIL import Image, ImageOps
import pillow_heif
sys.path.insert(0, os.path.dirname(__file__))
from crop import crop_to_paper, colors

pillow_heif.register_heif_opener()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
works = json.load(open("works.json"))
by_id = {w["id"]: w for w in works}
log = []

def save_sizes(im, wid, entry):
    full = im.copy(); full.thumbnail((2000, 2000), Image.LANCZOS)
    full.save(f"public/art/full/{wid}.jpg", quality=86, optimize=True, progressive=True)
    th = im.copy(); th.thumbnail((640, 640), Image.LANCZOS)
    th.save(f"public/art/thumb/{wid}.jpg", quality=80, optimize=True, progressive=True)
    entry.update(w=full.width, h=full.height, tw=th.width, th=th.height)

# ---- 1. new uploads
new = []
os.makedirs("originals", exist_ok=True)
for f in sorted(glob.glob("inbox/*")):
    if os.path.basename(f).startswith("."): continue
    try:
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
    except Exception as e:
        log.append(f"skipped {f}: {e}"); os.remove(f); continue
    wid = str(max(int(w["id"]) for w in works) + 1)
    cropped, found = crop_to_paper(im)
    entry = {"id": wid, "title": "", "added": os.path.basename(f)[:8], "cropped": found}
    save_sizes(cropped, wid, entry)
    entry.update(colors(cropped))
    works.insert(0, entry); by_id[wid] = entry; new.append(wid)
    shutil.move(f, f"originals/{wid}{os.path.splitext(f)[1].lower()}")
    log.append(f"added {wid} ({'cropped' if found else 'no paper edge found, kept whole photo'})")

# ---- 2. published edits
for p in sorted(glob.glob("edits/pending-*.json")):
    for e in json.load(open(p)):
        w = by_id.get(str(e.get("id")))
        if not w: continue
        turn = int(e.get("turn") or 0) % 360
        if turn:
            for k, q in (("full", 86), ("thumb", 80)):
                path = f"public/art/{k}/{w['id']}.jpg"
                im = Image.open(path).rotate(-turn, expand=True)
                im.save(path, quality=q, optimize=True, progressive=True)
                if k == "full": w["w"], w["h"] = im.size
                else: w["tw"], w["th"] = im.size
            w["rot"] = (w.get("rot", 0) + turn) % 360
        if "title" in e and e["title"] is not None: w["title"] = str(e["title"]).strip()[:120]
        if "hidden" in e: w["hidden"] = bool(e["hidden"])
        log.append(f"edited {w['id']}: turn {turn}, title {w.get('title')!r}, hidden {w.get('hidden', False)}")
    os.remove(p)

json.dump(works, open("works.json", "w"), indent=1)
subprocess.run([sys.executable, "build.py"], check=True)
print("\n".join(log) or "nothing to do")
open(os.environ.get("GITHUB_STEP_SUMMARY", os.devnull), "a").write("### deano.art update\n" + "\n".join(f"- {l}" for l in log) + "\n")
