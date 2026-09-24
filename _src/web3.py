"""Web entry flow: public landing page, sign in (centred card over a landscape), two-step verification."""
from __future__ import annotations

from charts import P4FP_DISTRICTS, UgandaMap
from kit import (AMBER, AMBER_D, CARD, FAINT, GREEN, GREEN_D, GREEN_M, INK, INK2, LEARN, LEVERAGE, LINE, LINE2, LINK,
                 MUTED, STATUS, SVG, button, checkbox, chip, field, logo_mark, para, tint, tw)
from mobile2 import landscape
from web import H, W


def top_nav(s: SVG, dark=False, active="Home"):
    fg = "#FFFFFF" if dark else INK
    with s.g("site header"):
        if not dark:
            s.rect(0, 0, W, 80, fill=CARD)
            s.line(0, 80, W, 80, LINE)
        logo_mark(s, 160, 20, 40)
        s.text(212, 40, "P4FP Uganda", 18, 700, fg)
        s.text(212, 60, "Power for Food Partnership · MEL", 12.5, 400, "#CFE3D7" if dark else MUTED)
        x = 700
        for lab in ["Home", "The programme", "Results", "Map", "Knowledge"]:
            on = lab == active
            s.text(x, 46, lab, 15, 600 if on else 400, (AMBER if dark else GREEN) if on else fg)
            if on:
                s.rect(x, 58, tw(lab, 15, 600), 3, fill=AMBER if dark else GREEN, rx=1.5)
            x += tw(lab, 15, 600) + 44
        button(s, W - 160, 20, "Sign in", "primary", icon="user", anchor="end", color=AMBER if dark else GREEN)
        s.link(W - 160 - 120, 20, 120, 40, "w01")


def w00_landing():
    s = SVG(W, H, "00 Public landing page")
    s.rect(0, 0, W, H, fill="#F4F6F2", name="page background")
    with s.g("hero"):
        s.rect(0, 0, W, 620, fill=GREEN_D, name="hero bg")
        s.circle(1500, 330, 330, fill="#FFFFFF", op=0.03)
    top_nav(s, dark=True)
    with s.g("hero copy"):
        s.text(160, 190, "SNV  ·  IKEA FOUNDATION  ·  2025–2029", 13, 700, AMBER, spacing=1.5)
        for i, ln in enumerate(["Clean energy and", "regenerative farming,", "measured on the farm."]):
            s.text(160, 262 + i * 64, ln, 54, 700, AMBER if i == 2 else "#FFFFFF", name=f"headline {i + 1}")
        para(s, 160, 440, "The Power for Food Partnership helps smallholder farmers and agribusinesses in 15 Ugandan "
                          "districts adopt regenerative practices powered by renewable energy. These are the programme's "
                          "approved results.", 620, 17, 400, "#D8E8DE", lh=27)
        button(s, 160, 548, "Sign in to the MEL platform", "primary", icon="arrowright", h=50, size=15, color=AMBER)
        s.link(160, 548, 290, 50, "w01")
        bw = tw("Explore the results map", 15, 600) + 62
        s.rect(470, 548, bw, 50, fill="none", rx=8, stroke="#FFFFFF", sw=1.2)
        s.icon("map", 486, 564, 18, "#FFFFFF", 2)
        s.text(514, 578, "Explore the results map", 15, 600, "#FFFFFF")
    # map on dark
    m = UgandaMap(1060, 100, 640, 500)
    with s.g("hero map"):
        for n in m.districts:
            if n not in P4FP_DISTRICTS:
                s.path(m.d(n), fill="#1C5A3D", stroke="#2B6B4C", sw=0.7, name=n)
        for n in P4FP_DISTRICTS:
            s.path(m.d(n), fill=AMBER, op=0.92, stroke=GREEN_D, sw=1, name=n)
        for n in ["Lira", "Mbale", "Mbarara", "Masaka", "Kasese"]:
            x, y = m.centroid(n)
            s.text(x + 10, y + 4, n, 12, 600, "#FFFFFF", name=f"label {n}")
    with s.g("map legend"):
        s.rect(1660, 520, 14, 14, fill=AMBER, rx=3)
        s.text(1682, 532, "15 programme districts", 12.5, 400, "#D8E8DE")

    # stats strip
    with s.g("results strip"):
        s.rect(160, 640, 1600, 150, fill=CARD, rx=16, stroke=LINE)
        stats = [("18,420", "farmers adopting RA-PURE practices", "54% women"),
                 ("312", "agribusinesses using renewable energy", "38% women-led"),
                 ("1,146", "solar irrigation & processing units", "installed"),
                 ("8,960 ha", "under regenerative practices", "and growing"),
                 ("8 · 15", "implementing partners · districts", "4 regions")]
        cw = 1600 / 5
        for i, (v, lab, sub) in enumerate(stats):
            x = 160 + i * cw
            if i:
                s.line(x, 668, x, 762, LINE)
            s.text(x + 36, 704, v, 34, 700, GREEN_D)
            s.text(x + 36, 732, lab, 13.5, 400, INK2, maxw=cw - 50)
            s.text(x + 36, 754, sub, 12.5, 600, AMBER_D)
        s.icon("shield", 180, 800, 16, MUTED, 2)
        s.text(204, 813, "Approved, non-sensitive figures only · updated nightly from the MEL platform · Q3 2026",
               12.5, 400, MUTED)

    # pathways + stories
    y0 = 846
    for i, (p, col, t1, t2) in enumerate([
            ("LEARN", LEARN, "Evidence from practice", "Learning events, research and exchanges across the region"),
            ("LINK", LINK, "Actors working together", "Farmers, SMEs, financiers and government in one system"),
            ("LEVERAGE", LEVERAGE, "Policy & investment", "Budgets, policies and finance that outlast the programme")]):
        x = 160 + i * 356
        with s.g(f"pathway {p}"):
            s.rect(x, y0, 340, 170, fill=CARD, rx=14, stroke=LINE)
            s.rect(x, y0, 340, 6, fill=col, rx=3)
            chip(s, x + 24, y0 + 26, p, col, solid=True, h=24)
            s.text(x + 24, y0 + 88, t1, 18, 700, INK)
            para(s, x + 24, y0 + 114, t2, 292, 13.5, 400, INK2, lh=20)
    with s.g("latest stories"):
        x = 160 + 3 * 356
        s.rect(x, y0, 1760 - x, 170, fill=CARD, rx=14, stroke=LINE)
        s.text(x + 24, y0 + 36, "Latest from the field", 16, 700, INK)
        s.text(1736, y0 + 36, "Knowledge library →", 13, 600, GREEN, anchor="end")
        for k, (t, meta) in enumerate([("From tarpaulins to solar dryers: Masaka's coffee women", "Success story · Sep 2026"),
                                       ("Budgeting for PURE: a note for district production offices", "Policy brief · Jul 2026")]):
            yy = y0 + 70 + k * 50
            s.rect(x + 24, yy - 4, 40, 40, fill=tint(GREEN, 0.12), rx=8)
            s.icon("book" if k else "sun", x + 34, yy + 6, 20, GREEN, 1.8)
            s.text(x + 78, yy + 12, t, 14, 600, INK, maxw=1760 - x - 110)
            s.text(x + 78, yy + 31, meta, 12, 400, MUTED)
    s.text(W / 2, H - 22, "Implemented by SNV with ACSA · PELUM Uganda · NREP · ACME · CREEC · NOGAMU · NARO · USEA", 12.5,
           400, MUTED, anchor="middle")
    return s


def web_scene(s: SVG):
    """A calm, wide landscape: small sun, rolling fields, solar arrays and a few trees."""
    with s.g("landscape background"):
        s.rect(0, 0, W, H, fill="#E4EFE8", name="sky")
        s.circle(1580, 250, 150, fill=AMBER, op=0.12, name="sun glow")
        s.circle(1580, 250, 80, fill=AMBER, name="sun")
        s.path("M0 700 C 420 610, 900 700, 1300 640 S 1760 600, 1920 630 L1920 1080 L0 1080 Z", fill="#9CC48A",
               name="far hills")
        s.path("M0 800 C 500 730, 1000 820, 1500 760 S 1820 740, 1920 760 L1920 1080 L0 1080 Z", fill="#5FA56F",
               name="mid field")
        s.path("M0 900 C 600 850, 1200 930, 1920 870 L1920 1080 L0 1080 Z", fill="#2F8F5E", name="near field")
        for i in range(6):
            y = 930 + i * 26
            s.path(f"M0 {y} C 600 {y - 44}, 1200 {y + 30}, 1920 {y - 50}", stroke="#1E6B47", sw=3, sop=0.55,
                   name=f"crop row {i + 1}")
        for arr, (x0, y0, n) in enumerate([(210, 736, 6), (1330, 716, 5)]):
            for k in range(n):
                px, py = x0 + k * 62, y0 + (k % 2) * 3
                s.rect(px + 26, py + 36, 4, 22, fill="#27425F", name=f"post {arr}-{k}")
                s.path(f"M{px} {py + 36} L{px + 8} {py} L{px + 60} {py} L{px + 52} {py + 36} Z", fill="#2E5B8F",
                       stroke="#1F3A5C", sw=1.5, name=f"panel {arr}-{k}")
                s.line(px + 30, py + 1, px + 26, py + 35, "#6B9BD1", 1)
        for tx, ty, r in [(120, 690, 34), (176, 704, 24), (1790, 650, 38), (1730, 670, 26), (1040, 690, 22)]:
            s.rect(tx - 3, ty, 6, r * 1.1, fill="#5A4632", name="trunk")
            s.circle(tx, ty - r * 0.3, r, fill="#1E6B47", name="tree")


def entry_bg(s: SVG):
    web_scene(s)
    with s.g("top bar"):
        logo_mark(s, 48, 32, 40)
        s.text(100, 52, "P4FP MEL", 18, 700, INK)
        s.text(100, 70, "SNV · Power for Food Uganda", 12, 400, INK2)
        bw = tw("Back to home", 14, 600) + 50
        s.rect(W - 48 - bw, 32, bw, 40, fill=CARD, rx=20, op=0.9)
        s.icon("arrowleft", W - 48 - bw + 16, 43, 18, INK, 2)
        s.text(W - 48 - bw + 40, 57, "Back to home", 14, 600, INK)
        s.link(W - 48 - bw, 32, bw, 40, "w00")
    s.text(W / 2, H - 28, "Protected under Uganda's Data Protection and Privacy Act, 2019 · SNV owns all programme data",
           12.5, 600, "#FFFFFF", anchor="middle")


def w01_sign_in():
    s = SVG(W, H, "01 Sign in")
    entry_bg(s)
    cw, ch = 500, 632
    cx, cy = (W - cw) / 2, 150
    with s.g("sign-in card"):
        s.rect(cx + 6, cy + 10, cw, ch, fill="#000000", rx=20, op=0.12, name="shadow")
        s.rect(cx, cy, cw, ch, fill=CARD, rx=20)
        x = cx + 44
        s.text(x, cy + 70, "Welcome back", 30, 700, INK)
        s.text(x, cy + 100, "Sign in to the P4FP MEL platform", 15, 400, MUTED)
        y = cy + 130
        button(s, x, y, "SNV staff: continue with Microsoft", "secondary", icon="sparkle", w=cw - 88, h=48)
        s.link(x, y, cw - 88, 48, "w01b")
        y += 76
        s.line(x, y, x + 170, y, LINE)
        s.text(cx + cw / 2, y + 5, "partners", 12.5, 400, MUTED, anchor="middle")
        s.line(x + cw - 88 - 170, y, x + cw - 88, y, LINE)
        y += 24
        y += field(s, x, y, cw - 88, "Email or phone", "grace.akello@snv.org", h=48, icon="user") + 16
        y += field(s, x, y, cw - 88, "Password", "••••••••••••", h=48, icon="lock", suffix="Show") + 10
        from kit import checkbox as cb
        cb(s, x, y + 6, True)
        s.text(x + 28, y + 20, "Keep me signed in for 7 days", 13, 400, INK2)
        s.text(x + cw - 88, y + 20, "Forgot password?", 13, 600, GREEN, anchor="end")
        y += 48
        button(s, x, y, "Sign in", "primary", w=cw - 88, h=50, size=15)
        s.link(x, y, cw - 88, 50, "w01b")
        y += 76
        s.rect(x, y, cw - 88, 64, fill="#F5F8F4", rx=10)
        s.icon("users", x + 16, y + 20, 22, GREEN, 1.9)
        para(s, x + 52, y + 27, "New partner user? SNV or your MEL focal person sends you an invitation by email.",
             cw - 88 - 68, 12.5, 400, INK2, lh=18)
    return s


def w01b_otp():
    s = SVG(W, H, "01b Two-step verification")
    entry_bg(s)
    cw, ch = 500, 560
    cx, cy = (W - cw) / 2, 220
    with s.g("verification card"):
        s.rect(cx + 6, cy + 10, cw, ch, fill="#000000", rx=20, op=0.12, name="shadow")
        s.rect(cx, cy, cw, ch, fill=CARD, rx=20)
        x = cx + 44
        s.rect(x, cy + 40, 52, 52, fill=tint(GREEN, 0.12), rx=12)
        s.icon("shield", x + 13, cy + 53, 26, GREEN, 2)
        s.text(x, cy + 136, "Two-step verification", 26, 700, INK)
        para(s, x, cy + 166, "Enter the 6-digit code we sent by SMS to +256 77• ••• 212. It expires in 5 minutes.",
             cw - 88, 14.5, 400, MUTED, lh=22)
        bw = (cw - 88 - 5 * 12) / 6
        for i in range(6):
            bx = x + i * (bw + 12)
            filled = i < 5
            s.rect(bx, cy + 226, bw, 64, fill=CARD, rx=12, stroke=GREEN if i == 5 else ("#9AA59F" if filled else LINE),
                   sw=2 if i == 5 else 1.2, name=f"digit {i + 1}")
            if filled:
                s.text(bx + bw / 2, cy + 268, "73915"[i], 28, 600, INK, anchor="middle")
            else:
                s.rect(bx + bw / 2 - 1, cy + 244, 2, 28, fill=GREEN)
        from kit import checkbox as cb
        cb(s, x, cy + 318, True)
        s.text(x + 28, cy + 332, "Trust this computer for 30 days", 13.5, 400, INK2)
        button(s, x, cy + 364, "Verify and continue", "primary", icon="arrowright", w=cw - 88, h=50, size=15)
        s.link(x, cy + 364, cw - 88, 50, "w02")
        s.text(x, cy + 446, "Didn't get a code?", 13.5, 400, MUTED)
        s.text(x + tw("Didn't get a code?", 13.5) + 6, cy + 446, "Resend in 0:38", 13.5, 600, INK2)
        s.text(x, cy + 478, "Use an authenticator app instead", 13.5, 600, GREEN)
        s.text(x + cw - 88, cy + 478, "Not you? Sign out", 13.5, 600, MUTED, anchor="end")
        s.link(x + cw - 88 - 130, cy + 460, 130, 26, "w00")
    return s


SCREENS = [w00_landing, w01_sign_in, w01b_otp]
