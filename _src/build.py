"""Build every mockup as SVG (for Adobe XD) and optionally render PNG previews.

    python build.py            # SVGs only
    python build.py --png      # SVGs + PNG previews via headless Chrome
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import mobile  # noqa: E402
import web  # noqa: E402
import web2  # noqa: E402
import web3  # noqa: E402
import mobile2  # noqa: E402
import web4  # noqa: E402


def _order(fn):
    key = fn.__name__.split('_')[0]
    return (int(key[1:3]), key[3:])

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def slug(title: str) -> str:
    return title.lower().replace("&", "and").replace("(", "").replace(")", "").replace(",", "").replace(" ", "-") \
        .replace("·", "").replace("--", "-")


PROTO = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>P4FP MEL Prototype</title>
<style>
  :root { --bg:#161B18; --bar:#232A26; --ink:#E9EEEA; --muted:#9AA69F; --accent:#F0A12B; }
  html, body { margin:0; height:100%; background:var(--bg); color:var(--ink); font:14px "Segoe UI", system-ui, sans-serif; overflow:hidden; }
  body.fs #stage { inset:0; }
  body.fs #bar { transform:translateY(100%); transition:transform .25s; }
  body.fs.peek #bar { transform:none; }
  #stage { position:absolute; inset:0 0 44px 0; display:flex; align-items:center; justify-content:center; }
  #frame { position:relative; }
  #frame.mobile { border:10px solid #0B0E0C; border-radius:36px; box-shadow:0 0 0 2px #333; overflow:hidden; }
  #frame img { display:block; width:100%; height:100%; user-select:none; -webkit-user-drag:none; transition:opacity .15s; }
  #frame.loading img { opacity:.25; }
  #msg { position:absolute; inset:0; display:none; align-items:center; justify-content:center; text-align:center; color:#fff; background:rgba(22,27,24,.85); font-size:15px; padding:20px; }
  #frame.failed #msg { display:flex; }
  #ready { color:var(--muted); font-size:12.5px; }
  .hot { position:absolute; cursor:pointer; border-radius:6px; }
  .flash .hot, .show .hot { background:rgba(43,108,176,.18); outline:2px solid rgba(43,108,176,.7); }
  .flash .hot { transition:background .6s, outline-color .6s; }
  #bar { position:absolute; left:0; right:0; bottom:0; height:44px; background:var(--bar); display:flex; align-items:center; gap:10px; padding:0 14px; }
  #bar button, #bar select { background:#2E3732; color:var(--ink); border:1px solid #3B4640; border-radius:6px; height:30px; padding:0 10px; font:inherit; cursor:pointer; }
  #bar select { max-width:340px; }
  #bar .sp { flex:1; }
  #bar > * { white-space:nowrap; flex-shrink:0; }
  #bar .hint { overflow:hidden; text-overflow:ellipsis; flex-shrink:1; min-width:0; }
  @media (max-width:1500px) { #bar .hint { display:none; } }
  #bar .hint { color:var(--muted); font-size:12.5px; }
  #bar .pill { color:#161B18; background:var(--accent); border-radius:10px; padding:1px 8px; font-weight:600; font-size:12px; }
</style></head><body>
<div id="stage"><div id="frame"><img id="img" alt=""><div id="msg">This screen could not load. Check the internet connection, then press → or pick it again.</div></div></div>
<div id="bar">
  <button id="prev" title="Previous (←)">&#8592;</button>
  <select id="pick"></select>
  <button id="next" title="Next (→)">&#8594;</button>
  <button id="web">Web</button><button id="mob">Android app (Flutter)</button>
  <button id="fs" title="Full screen (F) · Esc to exit">&#x26F6; Full screen</button>
  <span id="ready"></span><span class="sp"></span>
  <span class="hint">← → keys · H hotspots · F full screen · Esc exit</span>
  <span class="pill">Illustrative data</span>
</div>
<script>
const SCREENS = __DATA__;
const AUTO = { m01: ['m02', 1800] };  // splash moves on by itself
const order = SCREENS.map(s => s.key);
const byKey = Object.fromEntries(SCREENS.map(s => [s.key, s]));
// Download every screen up front so the walkthrough keeps working if the connection drops.
const CACHE = {}; let loaded = 0;
SCREENS.forEach(s => {
  const im = new Image();
  im.onload = () => { loaded++; document.getElementById('ready').textContent =
    loaded === SCREENS.length ? '✓ Offline-ready' : `Loading ${loaded}/${SCREENS.length}…`; };
  im.src = s.src; CACHE[s.key] = im;
});
const img = document.getElementById('img'), frame = document.getElementById('frame'), pick = document.getElementById('pick');
let cur = null, showAll = location.search.includes('show');
SCREENS.forEach(s => { const o = document.createElement('option'); o.value = s.key; o.textContent = s.title; pick.appendChild(o); });
function fit() {
  if (!cur) return;
  const s = byKey[cur], st = document.getElementById('stage');
  const pad = s.mobile ? 60 : 16, bw = s.mobile ? 20 : 0;
  const k = Math.min((st.clientWidth - pad) / s.w, (st.clientHeight - pad) / s.h, s.mobile ? 1.1 : 1);
  frame.style.width = (s.w * k + bw) + 'px'; frame.style.height = (s.h * k + bw) + 'px';
}
function go(key, push = true) {
  if (!byKey[key]) key = order[0];
  cur = key; const s = byKey[key];
  frame.className = s.mobile ? 'mobile' : ''; if (showAll) frame.classList.add('show');
  const cached = CACHE[key];
  if (cached && cached.complete && cached.naturalWidth) { img.src = cached.src; }
  else {
    frame.classList.add('loading');
    img.onload = () => frame.classList.remove('loading', 'failed');
    img.onerror = () => { frame.classList.remove('loading'); frame.classList.add('failed'); };
    img.src = s.src;
  }
  frame.querySelectorAll('.hot').forEach(h => h.remove());
  s.links.forEach(([x, y, w, h, t]) => {
    if (!byKey[t]) return;
    const a = document.createElement('div'); a.className = 'hot'; a.title = byKey[t].title;
    Object.assign(a.style, { left: x / s.w * 100 + '%', top: y / s.h * 100 + '%', width: w / s.w * 100 + '%', height: h / s.h * 100 + '%' });
    a.onclick = e => { e.stopPropagation(); go(t); };
    frame.appendChild(a);
  });
  pick.value = key; fit();
  clearTimeout(window._auto); if (AUTO[key]) window._auto = setTimeout(() => go(AUTO[key][0]), AUTO[key][1]);
  if (push) history.replaceState(null, '', '#' + key);
}
frame.addEventListener('click', () => { frame.classList.add('flash'); setTimeout(() => frame.classList.remove('flash'), 700); });
function step(d) { const i = order.indexOf(cur); go(order[(i + d + order.length) % order.length]); }
document.getElementById('prev').onclick = () => step(-1);
document.getElementById('next').onclick = () => step(1);
document.getElementById('web').onclick = () => go('w00');
document.getElementById('mob').onclick = () => go('m01');
pick.onchange = () => go(pick.value);
addEventListener('keydown', e => {
  if (e.key === 'ArrowRight') step(1); else if (e.key === 'ArrowLeft') step(-1);
  else if (e.key.toLowerCase() === 'h') { showAll = !showAll; frame.classList.toggle('show', showAll); }
});
const fsBtn = document.getElementById('fs');
function toggleFs() { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
fsBtn.onclick = toggleFs;
document.addEventListener('fullscreenchange', () => {
  const on = !!document.fullscreenElement;
  document.body.classList.toggle('fs', on);
  fsBtn.innerHTML = on ? '&#x2715; Exit full screen' : '&#x26F6; Full screen';
  setTimeout(fit, 50);
});
// in full screen the bar hides; move the mouse to the bottom edge to bring it back
addEventListener('mousemove', e => document.body.classList.toggle('peek', e.clientY > innerHeight - 70));
addEventListener('keydown', e => { if (e.key.toLowerCase() === 'f' && e.target.tagName !== 'SELECT') toggleFs(); });
addEventListener('resize', fit);
go(location.hash.slice(1) || 'w00', false);
</script></body></html>
"""


def write_prototype(built):
    import json
    data = [{"key": key, "title": title, "src": f"{folder}/{name}.svg", "w": w, "h": h, "mobile": folder == "mobile",
             "links": links} for folder, name, w, h, path, key, title, links in built]
    with open(os.path.join(OUT, "prototype.html"), "w", encoding="utf-8") as f:
        f.write(PROTO.replace("__DATA__", json.dumps(data)))
    print("prototype.html", sum(len(d["links"]) for d in data), "hotspots")


def main():
    png = "--png" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    built = []
    for folder, fns in (("web", sorted(web3.SCREENS + web.SCREENS[1:] + web2.SCREENS + web4.SCREENS, key=_order)),
                        ("mobile", mobile2.FIRST + mobile.SCREENS + mobile2.LAST)):
        os.makedirs(os.path.join(OUT, folder), exist_ok=True)
        for fn in fns:
            if only and not any(o in fn.__name__ for o in only):
                continue
            s = fn()
            name = slug(s.title)
            path = os.path.join(OUT, folder, name + ".svg")
            s.save(path)
            built.append((folder, name, s.w, s.h, path, fn.__name__.split('_')[0], s.title, s.links))
            print(f"{folder}/{name}.svg  {os.path.getsize(path) // 1024} KB")
    if not only:
        write_prototype(built)
    if png:
        prev = os.path.join(OUT, "_previews")
        os.makedirs(prev, exist_ok=True)
        for folder, name, w, h, path, *_ in built:
            out = os.path.join(prev, f"{folder}-{name}.png")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            f"--window-size={w},{h}", f"--screenshot={out}", "file:///" + path.replace("\\", "/")],
                           capture_output=True, timeout=60)
            print("png", out)


if __name__ == "__main__":
    main()
