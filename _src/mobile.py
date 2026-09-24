"""Android field app screens, 360 x 800 artboards."""
from __future__ import annotations

from charts import P4FP_DISTRICTS, UgandaMap
from kit import (AMBER, AMBER_D, BG, CARD, FAINT, GREEN, GREEN_D, GREEN_M, INK, INK2, LEARN, LEVERAGE, LINE, LINE2,
                 LINK, MUTED, PATHWAY, STATUS, SVG, avatar, button, checkbox, chip, field, logo_mark, para, progress,
                 radio, shade, status_chip, tint, toggle, tw, wrap)

MW, MH = 360, 800
PAD = 16


def phone(title: str, bg=BG, dark_status=False):
    s = SVG(MW, MH, title)
    s.rect(0, 0, MW, MH, fill=bg, name="screen background")
    status_bar(s, dark_status)
    return s


def status_bar(s: SVG, dark=False):
    fg = "#FFFFFF" if dark else INK
    with s.g("status bar"):
        s.text(PAD, 18, "10:24", 12.5, 600, fg)
        # signal, wifi-off/ battery
        x = MW - PAD
        s.rect(x - 22, 8, 20, 10, fill="none", stroke=fg, sw=1.2, rx=2, name="battery")
        s.rect(x - 20, 10, 12, 6, fill=fg, rx=1)
        s.rect(x - 1.5, 11, 2, 4, fill=fg, rx=1)
        for i in range(4):
            h = 3 + i * 2.2
            s.rect(x - 52 + i * 5, 17 - h, 3, h, fill=fg, rx=0.8, op=1 if i < 2 else 0.3, name="signal bar")
        s.text(x - 64, 18, "E", 10.5, 700, fg, anchor="end", name="network")


def app_bar(s: SVG, title, back=True, sub=None, right=None, color=CARD, fg=INK):
    if back:
        s.link(0, 24, 56, 56, "m06")
    with s.g("app bar"):
        s.rect(0, 24, MW, 56, fill=color, name="app bar bg")
        if color == CARD:
            s.line(0, 80, MW, 80, LINE)
        x = PAD
        if back:
            s.icon("arrowleft", x, 40, 24, fg, 2)
            x += 40
        if sub:
            s.text(x, 48, title, 17, 600, fg)
            s.text(x, 66, sub, 12, 400, MUTED if fg == INK else "#CFE3D7")
        else:
            s.text(x, 58, title, 18, 600, fg)
        if right:
            s.icon(right, MW - PAD - 24, 40, 24, fg, 2)


def bottom_nav(s: SVG, active="Home"):
    items = [("Home", "home"), ("Capture", "plus"), ("Outcomes", "sprout"), ("Sync", "refresh"), ("Me", "user")]
    for i, tgt in enumerate(["m06", "m07", "m09", "m10", "m13"]):
        s.link(i * MW / 5, MH - 76, MW / 5, 76, tgt)
    with s.g("bottom navigation"):
        s.rect(0, MH - 76, MW, 76, fill=CARD, name="nav bg")
        s.line(0, MH - 76, MW, MH - 76, LINE)
        w = MW / len(items)
        for i, (lab, ic) in enumerate(items):
            cx = i * w + w / 2
            on = lab == active
            with s.g(f"tab {lab}"):
                if on:
                    s.rect(cx - 30, MH - 68, 60, 30, fill=tint(GREEN, 0.14), rx=15, name="indicator")
                s.icon(ic, cx - 11, MH - 64, 22, GREEN_D if on else INK2, 2)
                s.text(cx, MH - 24, lab, 11.5, 600 if on else 400, GREEN_D if on else INK2, anchor="middle")
                if lab == "Sync":
                    s.circle(cx + 14, MH - 64, 8, fill=AMBER)
                    s.text(cx + 14, MH - 60.5, "7", 10, 700, "#FFFFFF", anchor="middle")
        s.rect(MW / 2 - 54, MH - 8, 108, 4, fill=INK, rx=2, op=0.35, name="gesture bar")


def gesture_only(s: SVG, dark=False):
    s.rect(MW / 2 - 54, MH - 8, 108, 4, fill="#FFFFFF" if dark else INK, rx=2, op=0.5, name="gesture bar")


def m_field(s: SVG, y, label, value, placeholder=False, dropdown=False, icon=None, required=True, h=48, suffix=None):
    return field(s, PAD, y, MW - 2 * PAD, label, value, h=h, placeholder=placeholder, dropdown=dropdown, icon=icon,
                 required=required, suffix=suffix, size=15)


# =====================================================================================
def m05_sign_in():
    s = phone("M5 Unlock with PIN (returning user)", bg=CARD)
    logo_mark(s, MW / 2 - 28, 70, 56)
    s.text(MW / 2, 160, "Welcome back, Sarah", 20, 700, INK, anchor="middle")
    s.text(MW / 2, 184, "NOGAMU · Field officer", 13.5, 400, MUTED, anchor="middle")
    s.text(MW / 2, 236, "Enter your 6-digit PIN", 14, 600, INK2, anchor="middle")
    with s.g("pin dots"):
        for i in range(6):
            cx = MW / 2 - 75 + i * 30
            s.circle(cx, 266, 7, fill=GREEN if i < 4 else CARD, stroke=GREEN if i < 4 else "#C5CCC7", sw=1.8)
    with s.g("keypad"):
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "fp", "0", "del"]
        kw, kh = 88, 64
        x0 = (MW - 3 * kw - 2 * 16) / 2
        for i, k in enumerate(keys):
            cx = x0 + (i % 3) * (kw + 16)
            cy = 310 + (i // 3) * (kh + 12)
            if k == "fp":
                s.icon("fingerprint", cx + kw / 2 - 16, cy + kh / 2 - 16, 32, GREEN, 1.8)
            elif k == "del":
                s.icon("arrowleft", cx + kw / 2 - 12, cy + kh / 2 - 12, 24, INK2, 2)
            else:
                s.rect(cx, cy, kw, kh, fill="#F3F6F2", rx=kh / 2, name=f"key {k}")
                s.text(cx + kw / 2, cy + kh / 2 + 9, k, 26, 400, INK, anchor="middle")
    s.link(0, 300, MW, 320, "m06")
    with s.g("offline note"):
        s.rect(PAD, 634, MW - 2 * PAD, 64, fill=tint(AMBER, 0.12), rx=12)
        s.icon("wifioff", PAD + 14, 654, 22, AMBER_D, 2)
        s.text(PAD + 48, 660, "No internet? You can still sign in.", 13, 600, INK)
        s.text(PAD + 48, 680, "Last synced today 08:12 · data encrypted", 12, 400, INK2)
    s.text(MW / 2, 740, "Forgot PIN? Use password", 13.5, 600, GREEN, anchor="middle")
    s.link(MW / 2 - 100, 722, 200, 30, "m03")
    gesture_only(s)
    return s


def m06_home():
    s = phone("M6 Field home (offline)")
    with s.g("header"):
        s.rect(0, 24, MW, 150, fill=GREEN_D, name="header bg")
        s.text(PAD, 60, "Good morning,", 14, 400, "#CFE3D7")
        s.text(PAD, 86, "Sarah Nakato", 22, 700, "#FFFFFF")
        s.text(PAD, 108, "NOGAMU · Masaka & Mpigi", 13, 400, "#CFE3D7")
        s.icon("bell", MW - PAD - 24, 44, 24, "#FFFFFF", 2)
        s.circle(MW - PAD - 4, 46, 6, fill=AMBER)
        s.link(MW - PAD - 32, 36, 40, 40, "m12")
    with s.g("offline banner"):
        s.rect(PAD, 124, MW - 2 * PAD, 58, fill=CARD, rx=12, stroke=tint(AMBER, 0.6))
        s.circle(PAD + 28, 153, 16, fill=tint(AMBER, 0.2))
        s.icon("wifioff", PAD + 18, 143, 20, AMBER_D, 2)
        s.text(PAD + 54, 149, "You're offline", 14, 600, INK)
        s.text(PAD + 54, 168, "7 records saved on phone · will sync", 12, 400, MUTED)
        s.icon("chevright", MW - PAD - 28, 143, 20, MUTED)
        s.link(PAD, 124, MW - 2 * PAD, 58, "m10")
    s.text(PAD, 214, "Capture", 15, 700, INK)
    tiles = [("sprout", GREEN, "Farmer adoption", "RA-PURE practices"), ("flag", LINK, "Harvest outcome", "What changed?"),
             ("listcheck", LEARN, "Log activity", "Training, demo, visit"), ("camera", AMBER_D, "Evidence photo", "GPS-stamped")]
    tw_ = (MW - 2 * PAD - 12) / 2
    for i, (ic, col, t1, t2) in enumerate(tiles):
        x = PAD + (i % 2) * (tw_ + 12)
        y = 228 + (i // 2) * 108
        s.link(x, y, tw_, 96, ["m07", "m09", None, "m08"][i])
        with s.g(f"tile {t1}"):
            s.rect(x, y, tw_, 96, fill=CARD, rx=14, stroke=LINE)
            s.rect(x + 14, y + 14, 36, 36, fill=tint(col, 0.14), rx=10)
            s.icon(ic, x + 22, y + 22, 20, shade(col, 0.1), 2)
            s.text(x + 14, y + 70, t1, 14, 600, INK)
            s.text(x + 14, y + 87, t2, 11.5, 400, MUTED)
    s.text(PAD, 470, "My tasks", 15, 700, INK)
    s.text(MW - PAD, 470, "3", 13, 600, MUTED, anchor="end")
    tasks = [("arrowleft", STATUS["Returned"], "Returned: add photo", "Activity FFS-14 · solar dryer demo"),
             ("users", AMBER_D, "Check 2 possible duplicates", "Kyanamukaka farmer register"),
             ("calendar", LEARN, "Farmer field school", "Today 14:00 · Bukakata")]
    y = 484
    s.link(PAD, y, MW - 2 * PAD, 60, "m12")
    for ic, col, t1, t2 in tasks:
        with s.g(f"task {t1}"):
            s.rect(PAD, y, MW - 2 * PAD, 60, fill=CARD, rx=12, stroke=LINE)
            s.circle(PAD + 30, y + 30, 17, fill=tint(col, 0.14))
            s.icon(ic, PAD + 21, y + 21, 18, col, 2.2)
            s.text(PAD + 58, y + 26, t1, 14, 600, INK)
            s.text(PAD + 58, y + 45, t2, 12, 400, MUTED, maxw=240)
            s.icon("chevright", MW - PAD - 28, y + 20, 20, FAINT)
        y += 68
    bottom_nav(s, "Home")
    return s


def m07_adoption():
    s = phone("M7 Farmer adoption record", bg=CARD)
    app_bar(s, "Farmer adoption", sub="PHI 8 · step 2 of 3", right="more")
    progress(s, 0, 80, MW, 0.66, GREEN, h=3, bg=LINE2, name="step progress")
    y = 94
    with s.g("duplicate warning"):
        s.rect(PAD, y, MW - 2 * PAD, 118, fill=tint(STATUS["Returned"], 0.08), rx=12,
               stroke=tint(STATUS["Returned"], 0.45))
        s.icon("users", PAD + 14, y + 14, 20, STATUS["Returned"], 2)
        s.text(PAD + 44, y + 29, "Possible match found", 14, 600, INK)
        para(s, PAD + 44, y + 50, "Nakato Sarah · Kyanamukaka · reported by NOGAMU in Q2 2026", MW - 2 * PAD - 60, 12.5,
             400, INK2, lh=18)
        bw = (MW - 2 * PAD - 28 - 10) / 2
        button(s, PAD + 14, y + 76, "Same person", "secondary", w=bw, h=32, size=12.5)
        button(s, PAD + 24 + bw, y + 76, "Different", "secondary", w=bw, h=32, size=12.5)
    y += 132
    y += m_field(s, y, "Farmer name", "Nakato Sarah", icon="user") + 12
    y += m_field(s, y, "Phone", "0772 ··· 418", icon="phone") + 12
    with s.g("sex and age"):
        s.text(PAD, y + 14, "Sex", 13, 600, INK2)
        s.text(MW / 2 + 6, y + 14, "Age group", 13, 600, INK2)
        hw = (MW - 2 * PAD - 12) / 2
        for i, (lab, on) in enumerate([("Woman", True), ("Man", False)]):
            x = PAD + i * hw / 2
            s.rect(x, y + 22, hw / 2 - 2, 40, fill=GREEN if on else CARD, rx=8, stroke=None if on else "#CFD6D1")
            s.text(x + hw / 4 - 1, y + 47, lab, 13.5, 600, "#FFFFFF" if on else INK2, anchor="middle")
        x = MW / 2 + 6
        for i, (lab, on) in enumerate([("18–35", False), ("36+", True)]):
            xx = x + i * hw / 2
            s.rect(xx, y + 22, hw / 2 - 2, 40, fill=GREEN if on else CARD, rx=8, stroke=None if on else "#CFD6D1")
            s.text(xx + hw / 4 - 1, y + 47, lab, 13.5, 600, "#FFFFFF" if on else INK2, anchor="middle")
        y += 76
    s.text(PAD, y + 14, "Practices adopted", 13, 600, INK2)
    y += 24
    x = PAD
    for lab, on in [("Mulching", True), ("Composting", True), ("Solar irrigation", True), ("Cover crops", False),
                    ("Solar drying", False)]:
        w = tw(lab, 12.5, 600) + (38 if on else 24)
        if x + w > MW - PAD:
            x = PAD
            y += 38
        with s.g(f"practice {lab}"):
            s.rect(x, y, w, 30, fill=tint(GREEN, 0.12) if on else CARD, rx=15, stroke=GREEN if on else "#CFD6D1")
            if on:
                s.icon("check", x + 10, y + 8, 14, GREEN_D, 2.6)
            s.text(x + (28 if on else 12), y + 20, lab, 12.5, 600, GREEN_D if on else INK2)
        x += w + 8
    y += 46
    with s.g("gps card"):
        s.rect(PAD, y, MW - 2 * PAD, 76, fill="#F4F7F3", rx=12, stroke=LINE)
        s.rect(PAD + 10, y + 10, 72, 56, fill="#DDE8DF", rx=8, name="mini map")
        s.path(f"M{PAD + 14} {y + 50} C {PAD + 34} {y + 30}, {PAD + 54} {y + 58}, {PAD + 78} {y + 26}", stroke="#B9CDBE",
               sw=4)
        s.icon("pin", PAD + 34, y + 20, 22, STATUS["Returned"], 2.2)
        s.text(PAD + 96, y + 30, "Location captured", 14, 600, INK)
        s.text(PAD + 96, y + 50, "-0.3412, 31.7351 · ±6 m", 12.5, 400, MUTED)
        s.icon("check", MW - PAD - 30, y + 26, 20, STATUS["Approved"], 2.6)
    with s.g("footer"):
        s.rect(0, MH - 84, MW, 84, fill=CARD)
        s.line(0, MH - 84, MW, MH - 84, LINE)
        button(s, PAD, MH - 70, "Back", "secondary", w=100, h=48)
        button(s, PAD + 112, MH - 70, "Save offline", "primary", icon="check", w=MW - 2 * PAD - 112, h=48)
        s.link(PAD + 112, MH - 70, MW - 2 * PAD - 112, 48, "m10")
        s.link(PAD, MH - 70, 100, 48, "m06")
    gesture_only(s)
    return s


def m08_camera():
    s = phone("M8 Evidence photo with GPS", bg="#0F1512", dark_status=True)
    with s.g("viewfinder"):
        s.rect(0, 24, MW, 560, fill="#8FB7D6", name="sky")
        s.circle(270, 120, 34, fill="#FFE39A", op=0.9, name="sun")
        s.path("M0 330 C 90 300, 200 320, 360 290 L360 584 L0 584 Z", fill="#6E9A4E", name="field")
        for i in range(8):
            yy = 360 + i * 28
            s.path(f"M0 {yy} C 120 {yy - 16}, 240 {yy - 6}, 360 {yy - 30}", stroke="#557C3A", sw=6, sop=0.8,
                   name=f"crop row {i + 1}")
        s.rect(110, 238, 150, 92, fill="#1F3A5C", rx=4, name="solar dryer panel")
        s.rect(114, 242, 142, 84, fill="#2E5B8F", rx=3)
        for k in range(1, 4):
            s.line(114 + k * 35.5, 242, 114 + k * 35.5, 326, "#6B9BD1", 1)
        s.line(114, 284, 256, 284, "#6B9BD1", 1)
        s.rect(130, 330, 8, 50, fill="#2A2A2A")
        s.rect(232, 330, 8, 50, fill="#2A2A2A")
        s.rect(96, 368, 176, 40, fill="#C9A15A", rx=4, name="drying rack")
        s.rect(100, 372, 168, 32, fill="#7A4E2D", rx=3, name="coffee beans")
        # focus brackets
        for (x, y, dx, dy) in [(60, 180, 1, 1), (300, 180, -1, 1), (60, 460, 1, -1), (300, 460, -1, -1)]:
            s.path(f"M{x} {y + 22 * dy} L{x} {y} L{x + 22 * dx} {y}", stroke="#FFFFFF", sw=2.5)
    s.link(0, 24, 60, 56, "m06")
    s.link(MW / 2 - 40, 700, 80, 80, "m07")
    with s.g("top controls"):
        s.icon("x", PAD, 40, 24, "#FFFFFF", 2.2)
        s.rect(MW / 2 - 70, 36, 140, 32, fill="#000000", op=0.45, rx=16)
        s.text(MW / 2, 57, "Evidence photo", 13.5, 600, "#FFFFFF", anchor="middle")
    with s.g("gps stamp"):
        s.rect(PAD, 470, MW - 2 * PAD, 98, fill="#000000", op=0.55, rx=12)
        s.icon("pin", PAD + 12, 484, 18, "#FFB547", 2.2)
        s.text(PAD + 36, 498, "Kyanamukaka, Masaka", 14, 600, "#FFFFFF")
        s.text(PAD + 36, 518, "-0.3412, 31.7351 · ±5 m", 12.5, 400, "#E1E7E3")
        s.text(PAD + 36, 537, "24 Sep 2026 · 10:18 · Sarah Nakato", 12.5, 400, "#E1E7E3")
        s.text(PAD + 36, 556, "Stamped on photo · cannot be edited", 11.5, 400, "#B8C4BD")
    with s.g("attach to"):
        s.text(PAD, 612, "Attach to", 12.5, 600, "#B8C4BD")
        s.rect(PAD, 622, MW - 2 * PAD, 44, fill="#1E2823", rx=10)
        s.icon("listcheck", PAD + 12, 634, 20, "#FFFFFF", 2)
        s.text(PAD + 42, 649, "FFS-14 · Solar dryer demo", 13.5, 600, "#FFFFFF")
        s.icon("chevdown", MW - PAD - 30, 634, 20, "#B8C4BD", 2)
    with s.g("consent"):
        toggle(s, PAD, 680, True)
        s.text(PAD + 48, 695, "Consent recorded for people in photo", 12.5, 400, "#E1E7E3")
    with s.g("shutter row"):
        s.rect(PAD + 8, 718, 44, 44, fill="#2C3A33", rx=8, name="gallery thumb")
        s.icon("image", PAD + 18, 728, 24, "#FFFFFF", 1.8)
        s.circle(MW / 2, 740, 32, fill="none", stroke="#FFFFFF", sw=4, name="shutter ring")
        s.circle(MW / 2, 740, 25, fill="#FFFFFF", name="shutter")
        s.circle(MW - PAD - 30, 740, 22, fill="#2C3A33")
        s.icon("refresh", MW - PAD - 42, 728, 24, "#FFFFFF", 2)
    gesture_only(s, dark=True)
    return s


def m09_outcome():
    s = phone("M9 Harvest an outcome", bg=CARD)
    app_bar(s, "Harvest an outcome", sub="Draft saved on phone", right="more")
    y = 96
    s.text(PAD, y + 14, "What changed?", 13, 600, INK2)
    s.text(PAD + tw("What changed?", 13, 600) + 4, y + 14, "*", 13, 600, STATUS["Rejected"])
    y += 22
    with s.g("statement box"):
        s.rect(PAD, y, MW - 2 * PAD, 140, fill=CARD, rx=10, stroke=GREEN, sw=1.5)
        para(s, PAD + 14, y + 26, "Five SACCOs in Masaka began offering asset loans for solar dryers to coffee farmers, "
                                  "after the June dealer–SACCO meeting.", MW - 2 * PAD - 28, 14, 400, INK, lh=21)
        s.line(PAD, y + 100, MW - PAD, y + 100, LINE2)
        s.icon("mic", PAD + 14, y + 110, 20, GREEN, 2)
        s.text(PAD + 40, y + 125, "Voice note · 0:42", 12.5, 600, GREEN)
        s.text(MW - PAD - 14, y + 125, "Luganda ok", 12, 400, MUTED, anchor="end")
    y += 156
    s.text(PAD, y + 14, "Who changed?", 13, 600, INK2)
    y += 24
    x = PAD
    for lab, on in [("Financial institution", True), ("Farmer group", False), ("Local gov't", False),
                    ("Private sector", False)]:
        w = tw(lab, 12.5, 600) + 24
        if x + w > MW - PAD:
            x = PAD
            y += 38
        s.rect(x, y, w, 30, fill=tint(LINK, 0.12) if on else CARD, rx=15, stroke=LINK if on else "#CFD6D1",
               name=f"actor {lab}")
        s.text(x + 12, y + 20, lab, 12.5, 600, shade(LINK, 0.1) if on else INK2)
        x += w + 8
    y += 48
    hw = (MW - 2 * PAD - 10) / 2
    field(s, PAD, y, hw, "When", "Aug 2026", h=44, icon="calendar", size=14)
    field(s, PAD + hw + 10, y, hw, "Where", "Masaka", h=44, icon="pin", size=14)
    y += 80
    s.text(PAD, y + 14, "Evidence", 13, 600, INK2)
    y += 22
    with s.g("evidence thumbs"):
        for i in range(3):
            x = PAD + i * 72
            s.rect(x, y, 64, 64, fill=["#CFE0C9", "#D9E4EE", "#EFE3CC"][i], rx=10)
            s.icon(["image", "file", "image"][i], x + 20, y + 20, 24, INK2, 1.8)
        s.rect(PAD + 216, y, 64, 64, fill=CARD, rx=10, stroke="#B9C3BC", dash="5 4")
        s.icon("plus", PAD + 236, y + 20, 24, GREEN, 2.2)
    y += 82
    with s.g("sharing and consent"):
        s.text(PAD, y + 14, "Sharing", 13, 600, INK2)
        y += 22
        hw = (MW - 2 * PAD - 8) / 2
        for i, (lab, on) in enumerate([("Restricted", True), ("OK to share", False)]):
            x = PAD + i * (hw + 8)
            s.rect(x, y, hw, 38, fill=tint(STATUS["Rejected"], 0.08) if on else CARD, rx=8,
                   stroke=STATUS["Rejected"] if on else "#CFD6D1")
            s.icon("lock" if on else "globe", x + 12, y + 11, 16, STATUS["Rejected"] if on else MUTED, 2)
            s.text(x + 34, y + 24, lab, 13, 600, INK if on else INK2)
        y += 48
        checkbox(s, PAD, y, True, 16)
        s.text(PAD + 24, y + 13, "Consent recorded for people named", 12.5, 400, INK2)
    with s.g("footer"):
        s.rect(0, MH - 84, MW, 84, fill=CARD)
        s.line(0, MH - 84, MW, MH - 84, LINE)
        button(s, PAD, MH - 70, "Submit to MEL focal person", "primary", icon="send", w=MW - 2 * PAD, h=48)
        s.link(PAD, MH - 70, MW - 2 * PAD, 48, "m10")
    gesture_only(s)
    return s


def m10_sync():
    s = phone("M10 Sync queue")
    app_bar(s, "Sync", back=False, right="refresh")
    with s.g("sync status"):
        s.rect(PAD, 96, MW - 2 * PAD, 110, fill=GREEN_D, rx=14)
        s.icon("wifi", PAD + 16, 114, 22, "#FFFFFF", 2)
        s.text(PAD + 48, 131, "Back online · syncing", 16, 700, "#FFFFFF")
        s.text(PAD + 16, 160, "31 of 38 records uploaded", 13, 400, "#CFE3D7")
        progress(s, PAD + 16, 174, MW - 2 * PAD - 32, 31 / 38, AMBER, h=8, bg="#2F6B4E")
        s.text(MW - PAD - 16, 160, "82%", 13, 700, "#FFFFFF", anchor="end")
    s.text(PAD, 238, "Needs your attention", 14, 700, INK)
    with s.g("conflict item"):
        y = 250
        s.rect(PAD, y, MW - 2 * PAD, 112, fill=CARD, rx=12, stroke=tint(STATUS["Returned"], 0.5))
        s.icon("alert", PAD + 14, y + 14, 20, STATUS["Returned"], 2.2)
        s.text(PAD + 44, y + 29, "Farmer already on the server", 14, 600, INK)
        para(s, PAD + 44, y + 50, "Kato Joseph was added by a colleague yesterday. Keep one record.", MW - 2 * PAD - 60,
             12.5, 400, INK2, lh=18)
        bw = (MW - 2 * PAD - 58 - 8) / 2
        button(s, PAD + 44, y + 72, "Keep server", "secondary", w=bw, h=30, size=12.5)
        button(s, PAD + 52 + bw, y + 72, "Merge", "soft", w=bw, h=30, size=12.5)
    s.text(PAD, 394, "Queue", 14, 700, INK)
    items = [("sprout", "Adoption · Nakato Sarah", "Kyanamukaka · 09:52", "Queued"),
             ("camera", "Photo · FFS-14 solar dryer", "2.1 MB · 10:18", "Uploading"),
             ("listcheck", "Activity · Farmer field school", "Bukakata · 23 Sep", "Synced"),
             ("sprout", "Adoption · Ssempala Moses", "Kyanamukaka · 23 Sep", "Synced"),
             ("flag", "Outcome draft · SACCO loans", "Masaka · 22 Sep", "Synced")]
    y = 406
    for ic, t1, t2, st in items:
        with s.g(f"queue {t1}"):
            s.rect(PAD, y, MW - 2 * PAD, 56, fill=CARD, rx=12, stroke=LINE)
            s.rect(PAD + 10, y + 10, 36, 36, fill="#F1F4F0", rx=8)
            s.icon(ic, PAD + 18, y + 18, 20, INK2, 1.8)
            s.text(PAD + 56, y + 25, t1, 13.5, 600, INK, maxw=180)
            s.text(PAD + 56, y + 43, t2, 12, 400, MUTED)
            if st == "Uploading":
                progress(s, MW - PAD - 70, y + 26, 56, 0.6, LEARN, h=5)
            else:
                col = STATUS["Approved"] if st == "Synced" else STATUS["Under review"]
                s.icon("check" if st == "Synced" else "clock", MW - PAD - 32, y + 18, 20, col, 2.4)
        y += 62
    bottom_nav(s, "Sync")
    return s


def m11_partner():
    s = phone("M11 Partner snapshot (Partner MEL Focal Person)")
    with s.g("header"):
        s.rect(0, 24, MW, 128, fill=CARD, name="header bg")
        s.line(0, 152, MW, 152, LINE)
        avatar(s, PAD + 20, 64, 20, "BT", LEARN)
        s.text(PAD + 52, 60, "NREP", 17, 700, INK)
        s.text(PAD + 52, 79, "Brian Tumusiime · Partner MEL Focal Person", 12.5, 400, MUTED)
        s.icon("bell", MW - PAD - 24, 50, 24, INK2, 2)
        s.rect(PAD, 102, MW - 2 * PAD, 36, fill="#F1F4F0", rx=18)
        s.rect(PAD + 3, 105, (MW - 2 * PAD) / 2 - 3, 30, fill=CARD, rx=15, stroke=LINE)
        s.text(PAD + (MW - 2 * PAD) / 4, 125, "Q3 2026", 13, 600, INK, anchor="middle")
        s.text(PAD + 3 * (MW - 2 * PAD) / 4, 125, "Since 2025", 13, 400, MUTED, anchor="middle")
    with s.g("due card"):
        y = 168
        s.rect(PAD, y, MW - 2 * PAD, 96, fill=GREEN_D, rx=14)
        s.text(PAD + 16, y + 28, "Q3 report due in 6 days", 15, 700, "#FFFFFF")
        s.text(PAD + 16, y + 48, "Technical 80% · Financial 0%", 12.5, 400, "#CFE3D7")
        progress(s, PAD + 16, y + 64, 180, 0.4, AMBER, h=8, bg="#2F6B4E")
        button(s, MW - PAD - 16, y + 50, "Open", "primary", anchor="end", h=34, size=13, color=AMBER)
    kw = (MW - 2 * PAD - 10) / 2
    for i, (lab, val, sub, col) in enumerate([("Farmers adopting", "3,940", "44% of 9,000", GREEN),
                                             ("Outcomes approved", "12", "1 returned", LINK),
                                             ("Solar units", "388", "49% of 800", AMBER_D),
                                             ("Activities done", "18/26", "3 due this month", LEARN)]):
        x = PAD + (i % 2) * (kw + 10)
        y = 280 + (i // 2) * 104
        with s.g(f"kpi {lab}"):
            s.rect(x, y, kw, 94, fill=CARD, rx=12, stroke=LINE)
            s.rect(x, y + 14, 3, 24, fill=col, rx=1.5)
            s.text(x + 14, y + 30, lab, 12.5, 600, INK2)
            s.text(x + 14, y + 62, val, 24, 700, INK)
            s.text(x + 14, y + 82, sub, 11.5, 400, MUTED)
    with s.g("trend card"):
        y = 494
        s.rect(PAD, y, MW - 2 * PAD, 200, fill=CARD, rx=12, stroke=LINE)
        s.text(PAD + 14, y + 28, "Farmers adopting · per quarter", 13.5, 600, INK)
        vals = [220, 480, 610, 540, 700, 620, 1020]
        labs = ["Q1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3"]
        bw = (MW - 2 * PAD - 28) / len(vals)
        for i, v in enumerate(vals):
            h = 120 * v / 1100
            x = PAD + 14 + i * bw
            last = i == len(vals) - 1
            s.rect(x + 6, y + 170 - h, bw - 12, h, fill=GREEN if not last else tint(GREEN, 0.4), rx=4,
                   stroke=None if not last else GREEN, dash=None)
            s.text(x + bw / 2, y + 188, labs[i], 11, 400, MUTED, anchor="middle")
        s.text(MW - PAD - 14, y + 28, "Q3 pending", 11.5, 600, AMBER_D, anchor="end")
    bottom_nav(s, "Home")
    return s


def m12_notifications():
    s = phone("M12 Notifications and returned item", bg=CARD)
    app_bar(s, "Notifications", back=True, right="sliders")
    with s.g("returned card"):
        y = 96
        s.rect(PAD, y, MW - 2 * PAD, 244, fill=tint(STATUS["Returned"], 0.06), rx=14,
               stroke=tint(STATUS["Returned"], 0.45))
        status_chip(s, PAD + 14, y + 14, "Returned")
        s.text(MW - PAD - 14, y + 31, "20 Sep", 12, 400, MUTED, anchor="end")
        para(s, PAD + 14, y + 66, "Isingiro dairy cooperative adopted solar milk chilling", MW - 2 * PAD - 28, 15, 600, INK,
             lh=21)
        s.rect(PAD + 14, y + 104, MW - 2 * PAD - 28, 84, fill=CARD, rx=10)
        avatar(s, PAD + 34, y + 124, 12, "GA", GREEN)
        s.text(PAD + 52, y + 128, "Grace Akello · SNV MEL Reviewer", 12, 600, INK2)
        para(s, PAD + 26, y + 152, "Please add the cooperative's before/after spoilage records as evidence.",
             MW - 2 * PAD - 52, 12.5, 400, INK, lh=18)
        button(s, PAD + 14, y + 198, "Fix now", "primary", icon="edit", w=MW - 2 * PAD - 28, h=36, size=13.5)
        s.link(PAD + 14, y + 198, MW - 2 * PAD - 28, 36, "m09")
    items = [("clock", AMBER_D, "Q3 report due in 6 days", "Technical 80% · Financial not started", "Today"),
             ("check", STATUS["Approved"], "5 results approved", "Q3 technical report · SNV MEL Reviewer", "Yesterday"),
             ("sprout", LINK, "Outcome OH-052 under review", "Mbarara budget line for solar irrigation", "16 Sep"),
             ("book", LEARN, "New learning brief published", "What keeps farmers adopting after year one?", "12 Sep")]
    y = 360
    s.text(PAD, y + 4, "Earlier", 13, 600, MUTED)
    y += 16
    for ic, col, t1, t2, when in items:
        with s.g(f"notification {t1}"):
            s.circle(PAD + 18, y + 30, 18, fill=tint(col, 0.14))
            s.icon(ic, PAD + 8, y + 20, 20, col, 2.2)
            s.text(PAD + 48, y + 26, t1, 14, 600, INK, maxw=200)
            s.text(PAD + 48, y + 45, t2, 12, 400, MUTED, maxw=260)
            s.text(MW - PAD, y + 26, when, 11.5, 400, MUTED, anchor="end")
            s.line(PAD + 48, y + 64, MW - PAD, y + 64, LINE2)
        y += 72
    s.text(MW / 2, y + 22, "Also sent by SMS when you're offline", 12, 400, MUTED, anchor="middle")
    gesture_only(s)
    return s


SCREENS = [m05_sign_in, m06_home, m07_adoption, m08_camera, m09_outcome, m10_sync, m11_partner, m12_notifications]
