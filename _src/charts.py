"""Charts and the Uganda map, drawn as plain SVG shapes."""
from __future__ import annotations

import json
import os
import math
import random

from kit import (AMBER, CARD, FAINT, GREEN, INK, INK2, LINE, LINE2, MUTED, REGION, SIGNALS, SVG, shade, tint, tw)

# Uganda district boundaries (UBOS, 137 districts), copied from the SDS tool so the repo builds on its own.
BOUNDARIES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "districts.geojson")

P4FP_DISTRICTS = {
    "Masaka": "Central", "Mpigi": "Central", "Mubende": "Central", "Luwero": "Central",
    "Nakasongola": "Central", "Kayunga": "Central",
    "Mbarara": "Western", "Kabarole": "Western", "Isingiro": "Western", "Kasese": "Western", "Ntungamo": "Western",
    "Mbale": "Eastern", "Iganga": "Eastern", "Jinja": "Eastern",
    "Lira": "Lango",
}

# Illustrative adoption counts (farmers adopting RA-PURE practices, cumulative)
ADOPTION = {
    "Masaka": 2140, "Mpigi": 980, "Mubende": 1320, "Luwero": 1610, "Nakasongola": 760, "Kayunga": 1190,
    "Mbarara": 2480, "Kabarole": 1050, "Isingiro": 1730, "Kasese": 890, "Ntungamo": 1270,
    "Mbale": 1460, "Iganga": 640, "Jinja": 920, "Lira": 1580,
}

# Which partners work where (illustrative operational areas)
PARTNER_AREAS = {
    "NREP": ["Mbarara", "Isingiro", "Ntungamo", "Lira"],
    "NOGAMU": ["Masaka", "Mpigi", "Luwero", "Kayunga"],
    "PELUM Uganda": ["Mubende", "Nakasongola", "Kabarole", "Kasese"],
    "CREEC": ["Mbale", "Jinja", "Iganga"],
    "USEA": ["Mbarara", "Masaka", "Lira", "Mbale", "Kasese"],
    "NARO": ["Mbarara", "Kabarole", "Masaka"],
    "ACSA": ["Luwero", "Nakasongola", "Lira"],
    "ACME": ["Masaka", "Mbarara", "Mbale", "Lira"],
}


# ---------------------------------------------------------------- radar
def radar(s: SVG, cx, cy, r, series, labels=True, max_v=4, label_size=12, rings=4, short=False):
    """series: [(values[8], color, name, filled)]."""
    n = len(SIGNALS)

    def pt(i, v):
        a = -math.pi / 2 + i * 2 * math.pi / n
        return cx + math.cos(a) * r * v / max_v, cy + math.sin(a) * r * v / max_v

    with s.g("radar chart"):
        with s.g("grid"):
            for k in range(1, rings + 1):
                s.poly([pt(i, max_v * k / rings) for i in range(n)], stroke=LINE if k < rings else "#D3DAD5",
                       sw=1, name=f"ring {k}")
            for i in range(n):
                x, y = pt(i, max_v)
                s.line(cx, cy, x, y, LINE2)
            for k in range(1, rings + 1):
                s.text(cx + 4, cy - r * k / rings + 12, str(k), 10, 400, FAINT, name=f"scale {k}")
        for vals, color, name, filled in series:
            with s.g(f"series {name}"):
                s.poly([pt(i, v) for i, v in enumerate(vals)], fill=color if filled else "none",
                       op=0.16 if filled else None, stroke=color, sw=2.2 if filled else 1.6,
                       dash=None if filled else "5 4", name="shape")
                if filled:
                    for i, v in enumerate(vals):
                        x, y = pt(i, v)
                        s.circle(x, y, 3.5, fill=CARD, stroke=color, sw=2)
        if labels:
            with s.g("axis labels"):
                for i, (code, lbl) in enumerate(SIGNALS):
                    a = -math.pi / 2 + i * 2 * math.pi / n
                    lx, ly = cx + math.cos(a) * (r + 18), cy + math.sin(a) * (r + 18)
                    c = math.cos(a)
                    anchor = "middle" if abs(c) < 0.3 else ("start" if c > 0 else "end")
                    dy = -6 if math.sin(a) < -0.5 else (14 if math.sin(a) > 0.5 else 4)
                    s.text(lx, ly + dy, code, label_size, 700, INK, anchor=anchor, name=code)
                    if not short:
                        s.text(lx, ly + dy + label_size + 3, lbl, label_size - 1, 400, MUTED, anchor=anchor,
                               name=f"{code} name")


# ---------------------------------------------------------------- donut
def arc_path(cx, cy, r_out, r_in, a0, a1):
    large = 1 if a1 - a0 > math.pi else 0
    x0, y0 = cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)
    x1, y1 = cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)
    x2, y2 = cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)
    x3, y3 = cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)
    return (f"M{x0:.2f} {y0:.2f} A{r_out} {r_out} 0 {large} 1 {x1:.2f} {y1:.2f} "
            f"L{x2:.2f} {y2:.2f} A{r_in} {r_in} 0 {large} 0 {x3:.2f} {y3:.2f} Z")


def donut(s: SVG, cx, cy, r, thick, parts, gap=0.025, name="donut"):
    """parts: [(value, color, label)]"""
    tot = sum(p[0] for p in parts)
    a = -math.pi / 2
    with s.g(name):
        for v, color, label in parts:
            da = 2 * math.pi * v / tot
            s.path(arc_path(cx, cy, r, r - thick, a + gap / 2, a + da - gap / 2), fill=color, name=label)
            a += da


# ---------------------------------------------------------------- line / area
def line_chart(s: SVG, x, y, w, h, series, xlabels, y_max, y_step, fmt=lambda v: f"{v:,.0f}", name="line chart"):
    """series: [(values, color, label, area)]"""
    with s.g(name):
        steps = int(y_max / y_step)
        for k in range(steps + 1):
            yy = y + h - h * k / steps
            s.line(x + 44, yy, x + w, yy, LINE2 if k else LINE)
            s.text(x + 36, yy + 4, fmt(k * y_step), 11, 400, MUTED, anchor="end", name="y label")
        n = len(xlabels)
        px = lambda i: x + 44 + (w - 44) * (i + 0.5) / n
        for i, lb in enumerate(xlabels):
            s.text(px(i), y + h + 20, lb, 11, 400, MUTED, anchor="middle", name="x label")
        for vals, color, label, area in series:
            pts = [(px(i), y + h - h * v / y_max) for i, v in enumerate(vals) if v is not None]
            with s.g(f"series {label}"):
                if area:
                    d = f"M{pts[0][0]:.1f} {y + h:.1f} " + " ".join(f"L{a:.1f} {b:.1f}" for a, b in pts) + \
                        f" L{pts[-1][0]:.1f} {y + h:.1f} Z"
                    s.path(d, fill=color, op=0.12, name="area")
                s.poly(pts, stroke=color, sw=2.4, closed=False, name="line",
                       dash=None if area or label != "Target" else "6 5")
                if area:
                    for a, b in pts:
                        s.circle(a, b, 3.5, fill=CARD, stroke=color, sw=2)


# ---------------------------------------------------------------- map
def _rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return _rdp(pts[: idx + 1], eps)[:-1] + _rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


_geo = None


def _load():
    global _geo
    if _geo is None:
        with open(BOUNDARIES, encoding="utf-8") as f:
            _geo = json.load(f)["features"]
    return _geo


class UgandaMap:
    LON0, LON1, LAT0, LAT1 = 29.55, 35.02, -1.50, 4.25

    def __init__(self, x, y, w, h, pad=8):
        self.x, self.y = x, y
        sx = (w - 2 * pad) / (self.LON1 - self.LON0)
        sy = (h - 2 * pad) / (self.LAT1 - self.LAT0)
        self.k = min(sx, sy)
        mw = (self.LON1 - self.LON0) * self.k
        mh = (self.LAT1 - self.LAT0) * self.k
        self.ox = x + (w - mw) / 2
        self.oy = y + (h - mh) / 2
        self.districts = {}
        for f in _load():
            ring = f["geometry"]["coordinates"][0]
            pts = [self.proj(lon, lat) for lon, lat in ring]
            mid = len(pts) // 2
            simp = _rdp(pts[: mid + 1], 0.35)[:-1] + _rdp(pts[mid:], 0.35)
            self.districts[f["properties"]["name"]] = (pts, simp)

    def proj(self, lon, lat):
        return self.ox + (lon - self.LON0) * self.k, self.oy + (self.LAT1 - lat) * self.k

    def d(self, name):
        pts = self.districts[name][1]
        return "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z"

    def centroid(self, name):
        pts = self.districts[name][0]
        a = cx = cy = 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            c = x0 * y1 - x1 * y0
            a += c
            cx += (x0 + x1) * c
            cy += (y0 + y1) * c
        a *= 0.5
        if abs(a) < 1e-6:
            xs, ys = zip(*pts)
            return sum(xs) / len(xs), sum(ys) / len(ys)
        return cx / (6 * a), cy / (6 * a)

    def inside(self, name, px, py):
        pts = self.districts[name][0]
        c = False
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            if (y0 > py) != (y1 > py) and px < (x1 - x0) * (py - y0) / (y1 - y0 + 1e-12) + x0:
                c = not c
        return c

    def random_points(self, name, n, seed=1):
        rnd = random.Random(seed * 1000 + sum(map(ord, name)))
        xs, ys = zip(*self.districts[name][0])
        out, tries = [], 0
        while len(out) < n and tries < 2000:
            tries += 1
            px, py = rnd.uniform(min(xs), max(xs)), rnd.uniform(min(ys), max(ys))
            if self.inside(name, px, py):
                out.append((px, py))
        return out

    def draw_base(self, s: SVG, fill="#E9EDE8", stroke="#FFFFFF", sw=0.8, name="Uganda districts"):
        with s.g(name):
            for n in self.districts:
                if n not in P4FP_DISTRICTS:
                    s.path(self.d(n), fill=fill, stroke=stroke, sw=sw, name=n)

    def draw_programme(self, s: SVG, mode="region", sw=1.2, name="P4FP districts", highlight=None):
        with s.g(name):
            mx = max(ADOPTION.values())
            for n, reg in P4FP_DISTRICTS.items():
                if mode == "region":
                    fill, op = REGION[reg], 0.78
                elif mode == "adoption":
                    fill, op = GREEN, 0.25 + 0.7 * ADOPTION[n] / mx
                else:
                    fill, op = tint(GREEN, 0.25), None
                if highlight and n not in highlight:
                    fill, op = "#DCE3DD", None
                s.path(self.d(n), fill=fill, op=op, stroke="#FFFFFF", sw=sw, name=n)

    def labels(self, s: SVG, size=11, names=None, color=INK, weight=600, halo=True):
        with s.g("district labels"):
            for n in names or P4FP_DISTRICTS:
                x, y = self.centroid(n)
                if halo:
                    w = tw(n, size, weight)
                    s.rect(x - w / 2 - 4, y - size + 1, w + 8, size + 6, fill="#FFFFFF", rx=4, op=0.85,
                           name="label bg")
                s.text(x, y + 2, n, size, weight, color, anchor="middle", name=n)
