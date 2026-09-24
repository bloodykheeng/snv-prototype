"""Web screens, 1920 x 1080 artboards."""
from __future__ import annotations

import math

from charts import ADOPTION, P4FP_DISTRICTS, PARTNER_AREAS, UgandaMap, donut, line_chart, radar
from kit import (AMBER, AMBER_D, BG, CARD, FAINT, GREEN, GREEN_D, GREEN_M, INK, INK2, LEARN, LEVERAGE, LINE, LINE2,
                 LINK, MUTED, PARTNERS, PATHWAY, REGION, SIGNALS, STATUS, SVG, avatar, button, card, checkbox, chip,
                 field, logo_mark, para, progress, radio, shade, status_chip, table, tint, toggle, tw, wrap)

W, H = 1920, 1080
SB = 264
TOP = 68
X0 = SB + 32
X1 = W - 32
CW = X1 - X0
Y0 = TOP + 28

SNV_USER = ("Grace Akello", "SNV MEL Reviewer", "GA")
PARTNER_USER = ("Brian Tumusiime", "Partner MEL Focal Person", "BT")

NAV_SNV = [
    ("PROGRAMME", [("Overview", "grid"), ("Indicators", "target"), ("Outcome harvesting", "sprout"),
                   ("System Signals", "radar"), ("GIS & maps", "map")]),
    ("PARTNERS", [("Partner reporting", "file"), ("Review queue", "workflow"),
                  ("Workplans & milestones", "listcheck")]),
    ("KNOWLEDGE", [("Knowledge library", "book"), ("Evidence store", "clip")]),
    ("ADMINISTRATION", [("LogAlto & exports", "database"), ("Users & roles", "users"), ("Audit trail", "history")]),
]
NAV_PARTNER = [
    ("NREP WORKSPACE", [("My dashboard", "home"), ("Quarterly reports", "file"), ("Indicators", "target"),
                        ("Outcomes", "sprout"), ("Workplan & sub-grant", "listcheck"), ("Evidence", "clip")]),
    ("SHARED", [("Knowledge library", "book"), ("Programme map", "map")]),
]
NAV_TARGET = {"Overview": "w02", "Indicators": "w03", "Outcome harvesting": "w06", "System Signals": "w08",
              "GIS & maps": "w09", "Partner reporting": "w04", "Review queue": "w05", "Workplans & milestones": "w16",
              "Knowledge library": "w12", "Evidence store": "w15", "LogAlto & exports": "w13", "Users & roles": "w14",
              "Audit trail": "w17", "My dashboard": "w10", "Quarterly reports": "w11", "Outcomes": "w06",
              "Workplan & sub-grant": "w10", "Evidence": "w11", "Programme map": "w09"}
BADGES = {"Review queue": "9", "Quarterly reports": "1", "Outcomes": "1"}


NAV_TARGET_PARTNER = {"My dashboard": "w10", "Quarterly reports": "w11", "Indicators": "w10b", "Outcomes": "w10c",
                      "Workplan & sub-grant": "w10", "Evidence": "w11", "Knowledge library": "w12p",
                      "Programme map": "w09p"}
PARTNER_MODE = {"on": False}  # set by web4 to render a shared screen inside the partner shell
PARTNER_ACTIVE = {"GIS & maps": "Programme map"}


def shell(title: str, active: str, crumbs: list[str], user=SNV_USER, nav=NAV_SNV, period="Q3 2026 · Jul–Sep"):
    if PARTNER_MODE["on"]:
        user, nav = PARTNER_USER, NAV_PARTNER
        active = PARTNER_ACTIVE.get(active, active)
        crumbs = ["NREP"] + crumbs[1:]
    s = SVG(W, H, title)
    s.rect(0, 0, W, H, fill=BG, name="page background")

    with s.g("sidebar"):
        s.rect(0, 0, SB, H, fill=CARD, name="sidebar bg")
        s.line(SB, 0, SB, H, LINE)
        logo_mark(s, 24, 18, 36)
        s.text(70, 34, "P4FP MEL", 17, 700, INK, name="product name")
        s.text(70, 52, "SNV · Power for Food Uganda", 11.5, 400, MUTED, name="product sub")
        y = 96
        for group, items in nav:
            s.text(28, y, group, 10.5, 600, FAINT, spacing=1, name=f"nav group {group}")
            y += 14
            for label, ic in items:
                on = label == active
                with s.g(f"nav {label}"):
                    if on:
                        s.rect(14, y, SB - 28, 40, fill=tint(GREEN, 0.1), rx=8, name="active bg")
                        s.rect(14, y + 10, 3, 20, fill=GREEN, rx=1.5, name="active bar")
                    s.icon(ic, 30, y + 10, 20, GREEN if on else INK2, 1.8)
                    s.text(62, y + 25, label, 14, 600 if on else 400, GREEN_D if on else INK2, name="label")
                    if label in BADGES:
                        b = BADGES[label]
                        bw = tw(b, 11, 700) + 14
                        s.rect(SB - 30 - bw, y + 11, bw, 18, fill=AMBER if label != "Review queue" else GREEN,
                               rx=9, name="badge")
                        s.text(SB - 30 - bw / 2, y + 24, b, 11, 700, "#FFFFFF", anchor="middle", name="badge n")
                s.link(14, y, SB - 28, 40, (NAV_TARGET_PARTNER if nav is NAV_PARTNER else NAV_TARGET).get(label))
                y += 42
            y += 14
        # offline-ready card
        with s.g("sidebar help card"):
            s.rect(16, H - 176, SB - 32, 84, fill=tint(AMBER, 0.12), rx=10)
            s.icon("phone", 30, H - 162, 20, AMBER_D, 1.8)
            s.text(58, H - 147, "Mobile field app", 13, 600, INK)
            s.text(30, H - 125, "Android app, built in Flutter.", 12, 400, INK2)
            s.text(30, H - 107, "Offline capture, GPS, photos.", 12, 400, INK2)
        s.link(0, H - 76, SB - 56, 76, "w10" if nav is NAV_SNV else "w02")  # demo: switch SNV <-> partner view
        s.link(SB - 52, H - 60, 40, 44, "w00")  # sign out
        with s.g("sidebar user"):
            s.line(0, H - 76, SB, H - 76, LINE)
            avatar(s, 44, H - 38, 18, user[2], GREEN if nav is NAV_SNV else LEARN)
            s.text(72, H - 42, user[0], 14, 600, INK)
            s.text(72, H - 23, user[1], 12, 400, MUTED, maxw=SB - 124)
            s.rect(SB - 50, H - 58, 38, 38, fill="#F4F6F3", rx=8, name="sign out button")
            s.icon("logout", SB - 41, H - 49, 20, STATUS["Rejected"], 2)

    with s.g("top bar"):
        s.rect(SB, 0, W - SB, TOP, fill=CARD, name="top bar bg")
        s.line(SB, TOP, W, TOP, LINE)
        x = X0
        for i, c in enumerate(crumbs):
            last = i == len(crumbs) - 1
            x += s.text(x, 40, c, 14, 600 if last else 400, INK if last else MUTED, name=f"crumb {c}")
            if not last:
                s.icon("chevright", x + 6, 29, 16, FAINT)
                x += 28
        # right side
        rx = X1
        avatar(s, rx - 18, 34, 18, user[2], GREEN if nav is NAV_SNV else LEARN)
        rx -= 52
        s.line(rx, 20, rx, 48, LINE)
        rx -= 44
        with s.g("notifications"):
            s.icon("bell", rx, 23, 22, INK2)
            s.circle(rx + 19, 25, 7, fill=STATUS["Overdue"])
            s.text(rx + 19, 29, "4", 10, 700, "#FFFFFF", anchor="middle")
        rx -= 320
        with s.g("search"):
            s.rect(rx, 16, 296, 36, fill="#F4F6F3", rx=8, stroke=LINE)
            s.icon("search", rx + 12, 25, 18, MUTED)
            s.text(rx + 40, 39, "Search indicators, outcomes, reports…", 13, 400, FAINT)
            s.rect(rx + 262, 24, 24, 20, fill=CARD, rx=4, stroke=LINE)
            s.text(rx + 274, 38, "/", 11, 600, MUTED, anchor="middle")
        pw = tw(period, 13, 600) + tw("Period", 12) + 84
        rx -= pw + 16
        with s.g("period selector"):
            s.rect(rx, 16, pw, 36, fill=CARD, rx=8, stroke=LINE)
            s.icon("calendar", rx + 12, 25, 18, GREEN)
            s.text(rx + 38, 39, "Period", 12, 400, MUTED)
            s.text(rx + 42 + tw("Period", 12), 39, period, 13, 600, INK)
            s.icon("chevdown", rx + pw - 26, 27, 16, MUTED)
    return s


def page_head(s: SVG, title, subtitle, y=Y0):
    s.text(X0, y + 30, title, 26, 700, INK, name="page title")
    s.text(X0, y + 56, subtitle, 14, 400, MUTED, name="page subtitle")


def approved_only_note(s: SVG, x, y):
    """The rule SNV cares about: only approved data counts."""
    w = tw("Showing approved data only", 12, 600) + 40
    with s.g("approved-only note"):
        s.rect(x, y, w, 28, fill=tint(STATUS["Approved"], 0.1), rx=14)
        s.icon("shield", x + 10, y + 6, 16, STATUS["Approved"], 2)
        s.text(x + 31, y + 18.5, "Showing approved data only", 12, 600, shade(STATUS["Approved"], 0.15))
    return w


def filter_btn(s: SVG, x, y, label, value, w=None):
    lw = tw(label + ":", 13)
    vw = tw(value, 13, 600)
    bw = w or lw + vw + 54
    with s.g(f"filter {label}"):
        s.rect(x, y, bw, 38, fill=CARD, rx=8, stroke=LINE)
        s.text(x + 14, y + 24, label + ":", 13, 400, MUTED)
        s.text(x + 18 + lw, y + 24, value, 13, 600, INK, maxw=bw - lw - 50)
        s.icon("chevdown", x + bw - 28, y + 11, 16, MUTED)
    return bw


def kpi(s: SVG, x, y, w, h, icon, color, label, value, sub, frac=None, tag=None, delta=None):
    with s.g(f"kpi {label}"):
        s.rect(x, y, w, h, fill=CARD, rx=12, stroke=LINE, name="bg")
        s.rect(x + 20, y + 20, 38, 38, fill=tint(color, 0.13), rx=9, name="icon bg")
        s.icon(icon, x + 29, y + 29, 20, shade(color, 0.1), 2)
        s.text(x + 70, y + 36, label, 13, 600, INK2, maxw=w - 90)
        if tag:
            chip(s, x + 70, y + 43, tag, color, h=20, size=11)
        vw = s.text(x + 20, y + 98, value, 30, 700, INK, name="value")
        if delta:
            s.icon("arrowupright", x + 28 + vw, y + 80, 16, STATUS["Approved"], 2.2)
            s.text(x + 46 + vw, y + 94, delta, 12, 600, STATUS["Approved"], name="delta")
        s.text(x + 20, y + 120, sub, 12.5, 400, MUTED, name="sub", maxw=w - 40)
        if frac is not None:
            progress(s, x + 20, y + h - 14, w - 40, frac, color, h=6)


# =====================================================================================
def w01_sign_in():
    s = SVG(W, H, "01 Sign in")
    s.rect(0, 0, W, H, fill=CARD, name="page background")
    with s.g("brand panel"):
        s.rect(0, 0, 880, H, fill=GREEN_D, name="brand bg")
        # abstract field rows + sun
        with s.g("illustration"):
            s.circle(690, 800, 150, fill=AMBER, op=0.12, name="sun glow")
            s.circle(690, 800, 100, fill=AMBER, op=0.95, name="sun")
            for i in range(7):
                yy = 900 + i * 34
                s.path(f"M0 {yy} C 240 {yy - 40}, 560 {yy - 20}, 880 {yy - 70 + i * 4}", stroke="#2F8F5E",
                       sw=14 - i, sop=0.6 - i * 0.05, name=f"field row {i + 1}")
            for k in range(5):
                px = 470 + k * 60
                py = 830 + (k % 2) * 8
                s.rect(px, py, 46, 70, fill="#0E3A26", rx=3, name=f"solar panel {k + 1}")
                s.rect(px + 3, py + 3, 40, 64, fill="#244F7D", rx=2)
                s.line(px + 23, py + 3, px + 23, py + 67, "#6B9BD1", 1)
                s.line(px + 3, py + 35, px + 43, py + 35, "#6B9BD1", 1)
                s.rect(px + 21, py + 70, 4, 22, fill="#0E3A26")
        logo_mark(s, 80, 72, 48)
        s.text(142, 96, "P4FP MEL Platform", 22, 700, "#FFFFFF")
        s.text(142, 118, "SNV · Power for Food Partnership Uganda", 14, 400, "#CFE3D7")
        s.text(80, 250, "Evidence for resilient,", 44, 700, "#FFFFFF", name="headline 1")
        s.text(80, 304, "renewable-energy-driven", 44, 700, "#FFFFFF", name="headline 2")
        s.text(80, 358, "food systems.", 44, 700, AMBER, name="headline 3")
        para(s, 80, 406, "One place for SNV and the eight implementing partners to report, review and learn — "
                         "from the farm plot in Isingiro to the programme dashboard.", 440, 16, 400, "#D8E8DE", lh=26)
        y = 520
        for ic, t in [("file", "Report once — partner reports feed dashboards and LogAlto"),
                      ("shield", "Only SNV-approved data reaches official figures"),
                      ("wifioff", "Works offline in the field, syncs when connected")]:
            s.rect(80, y - 20, 32, 32, fill="#FFFFFF", op=0.12, rx=8)
            s.icon(ic, 87, y - 13, 18, "#FFFFFF", 2)
            s.text(126, y + 1, t, 15, 400, "#FFFFFF")
            y += 50
        s.text(80, H - 48, "Funded by the IKEA Foundation · Implemented by SNV with ACSA, PELUM Uganda, NREP, ACME, "
                           "CREEC, NOGAMU, NARO and USEA", 12, 400, "#A9C9B5", name="footer credit")

    fx = 880 + (W - 880 - 440) / 2
    with s.g("sign-in form"):
        s.text(fx, 250, "Sign in", 32, 700, INK)
        s.text(fx, 282, "Use your SNV or partner account.", 15, 400, MUTED)
        button(s, fx, 318, "Continue with Microsoft (SNV staff)", "secondary", icon="sparkle", w=440, h=48)
        with s.g("divider"):
            s.line(fx, 400, fx + 190, 400, LINE)
            s.text(fx + 220, 405, "or", 13, 400, MUTED, anchor="middle")
            s.line(fx + 250, 400, fx + 440, 400, LINE)
        field(s, fx, 428, 440, "Email or phone", "brian.t@nrep.ug", h=48, icon="user")
        field(s, fx, 512, 440, "Password", "••••••••••••", h=48, icon="lock")
        s.text(fx + 440, 526, "Forgot password?", 13, 600, GREEN, anchor="end")
        checkbox(s, fx, 604, True)
        s.text(fx + 28, 618, "Keep me signed in on this device for 7 days", 13, 400, INK2)
        button(s, fx, 646, "Sign in", "primary", w=440, h=48, size=15)
        s.link(fx, 646, 440, 48, "w02")
        s.link(fx, 318, 440, 48, "w02")
        with s.g("2FA note"):
            s.rect(fx, 722, 440, 64, fill="#F6F8F5", rx=10, stroke=LINE)
            s.icon("fingerprint", fx + 16, 742, 22, GREEN, 1.8)
            s.text(fx + 52, 748, "Two-step verification is on", 13, 600, INK)
            s.text(fx + 52, 768, "We will text a 6-digit code to your phone next.", 12, 400, MUTED)
    s.text(880 + (W - 880) / 2, H - 48, "Protected under Uganda's Data Protection and Privacy Act, 2019 · "
                                         "SNV owns all programme data", 12, 400, MUTED, anchor="middle")
    return s


# =====================================================================================
INDICATORS = [
    ("Farmers adopting RA-PURE practices", "PHI 8 · SS5", 18420, 45000, 0.45, "54% women", "{:,}"),
    ("Hectares under regenerative practices", "OI 1.2", 8960, 20000, 0.45, None, "{:,} ha"),
    ("Agribusinesses / SMEs using PURE solutions", "OI 2.1", 312, 600, 0.45, "38% women-led", "{:,}"),
    ("Solar irrigation & processing units installed", "OI 2.3", 1146, 2500, 0.45, None, "{:,}"),
    ("People trained on RA-PURE (all actors)", "OI 3.1", 24870, 40000, 0.45, "57% women", "{:,}"),
    ("Multi-actor platforms & partnerships active", "OI 3.4", 23, 40, 0.45, None, "{:,}"),
    ("Finance mobilised for RA-PURE (EUR)", "OI 4.2", 1.9, 5.0, 0.45, None, "€{:.1f}M"),
]

PARTNER_STATUS = [
    # partner, technical, financial, evidence(x/y), workplan frac, focal, last
    ("ACSA", "Approved", "Approved", (9, 9), 0.72, "Ruth Nabirye", "12 Sep"),
    ("PELUM Uganda", "Approved", "Under review", (14, 15), 0.66, "Peter Okello", "18 Sep"),
    ("NREP", "Under review", "Submitted", (11, 12), 0.69, "Brian Tumusiime", "18 Sep"),
    ("ACME", "Approved", "Approved", (6, 6), 0.81, "Joan Atim", "10 Sep"),
    ("CREEC", "Returned", "Approved", (7, 10), 0.58, "Samuel Wasswa", "20 Sep"),
    ("NOGAMU", "Approved", "Under review", (16, 16), 0.75, "Harriet Nansubuga", "15 Sep"),
    ("NARO", "Submitted", "Draft", (4, 8), 0.54, "Dr. Moses Ekwaru", "22 Sep"),
    ("USEA", "Overdue", "Overdue", (0, 7), 0.41, "Kenneth Mugisha", "—"),
]


def w02_overview():
    s = shell("02 Programme overview (SNV)", "Overview", ["Programme", "Overview"])
    page_head(s, "Programme overview", "P4FP Uganda · 8 implementing partners · 15 districts in 4 regions · "
                                       "cumulative since January 2025")
    with s.g("header actions"):
        x = X1
        x -= button(s, x, Y0 + 12, "Export", "primary", icon="download", anchor="end") + 12
        x -= filter_btn(s, x - 190, Y0 + 13, "Value chain", "All", w=190) + 12
        x -= filter_btn(s, x - 150, Y0 + 13, "Region", "All", w=150) + 12
        x -= filter_btn(s, x - 160, Y0 + 13, "Pathway", "All", w=160) + 16
        approved_only_note(s, x - 214, Y0 + 18)

    ky = Y0 + 84
    kw = (CW - 4 * 20) / 5
    kpis = [
        ("sprout", GREEN, "Farmers adopting RA-PURE", "18,420", "of 45,000 target · 41%", 0.41, "SS5 · PHI 8", "+2,310"),
        ("zap", AMBER, "Agribusinesses using PURE", "312", "of 600 target · 52%", 0.52, "OI 2.1", "+41"),
        ("flag", LINK, "Outcomes harvested", "64", "approved · 9 awaiting SNV review", None, "SS1–SS8", "+11"),
        ("file", LEARN, "Partner reports · Q3", "6 of 8", "handed in · 1 returned · 1 overdue", 0.75, "Due 30 Sep", None),
        ("shield", "#0F766E", "Evidence coverage", "87%", "of results linked to evidence", 0.87, "Target 95%", None),
    ]
    for i, (ic, col, lab, val, sub, fr, tag, d) in enumerate(kpis):
        kpi(s, X0 + i * (kw + 20), ky, kw, 150, ic, col, lab, val, sub, fr, tag, d)

    for i, tgt in enumerate(["w03", "w03", "w06", "w04", "w05"]):
        s.link(X0 + i * (kw + 20), ky, kw, 150, tgt)
    # ---- indicator progress
    ry = ky + 170
    s.link(X0, ry, 1010, 360, "w03")
    s.link(X0 + 1030, ry, CW - 1030, 360, "w08")
    cx_, cy_ = card(s, X0, ry, 1010, 360, "Indicator progress against target",
                    "Bar = achieved (approved) · black tick = where we should be by now (45% of programme time)",
                    action="All 24 indicators →")
    with s.g("indicator bars"):
        y = cy_ + 6
        for name, code, val, tgt, mk, gesi, fmt in INDICATORS:
            fr = val / tgt
            col = GREEN if fr >= mk * 0.92 else AMBER
            s.text(cx_, y + 13, name, 13.5, 400, INK, maxw=330, name="indicator")
            chip(s, cx_ + 336, y - 2, code, LEARN if "PHI" not in code else GREEN, h=20, size=10.5)
            progress(s, cx_ + 440, y + 6, 290, fr, col, h=10, marker=mk)
            s.text(cx_ + 746, y + 15, fmt.format(val), 13.5, 600, INK, name="value")
            s.text(cx_ + 746 + tw(fmt.format(val), 13.5, 600) + 4, y + 15, "/ " + fmt.format(tgt), 12.5, 400, MUTED,
                   name="target")
            if gesi:
                s.text(cx_ + 962, y + 15, gesi, 12, 600, "#9D4A8C", anchor="end", name="gesi")
            y += 38

    # ---- radar
    rx0 = X0 + 1030
    rw = CW - 1030
    card(s, rx0, ry, rw, 360, "System Signals · SS1–SS8", "Sense Making scores (0–4) · approved 16 Sep 2026")
    with s.g("radar legend"):
        s.rect(rx0 + rw - 200, ry + 24, 14, 14, fill=GREEN, op=0.3, stroke=GREEN)
        s.text(rx0 + rw - 180, ry + 36, "Q3 2026", 12, 600, INK)
        s.line(rx0 + rw - 110, ry + 31, rx0 + rw - 94, ry + 31, AMBER_D, 2, dash="4 3")
        s.text(rx0 + rw - 88, ry + 36, "Baseline", 12, 400, INK2)
    radar(s, rx0 + rw / 2, ry + 204, 96, [
        ([1.5, 2.0, 1.0, 1.0, 1.5, 1.5, 2.0, 1.0], AMBER_D, "Baseline Q4 2025", False),
        ([2.5, 3.0, 2.0, 1.5, 2.5, 2.0, 3.0, 1.5], GREEN, "Q3 2026", True),
    ], label_size=11.5)

    # ---- bottom row
    by = ry + 380
    bh = H - 28 - by
    mw = 470
    card(s, X0, by, mw, bh, "Reach · RA-PURE adoption", "Farmers adopting, by district (approved)")
    m = UgandaMap(X0 + 12, by + 70, mw - 150, bh - 80)
    s.rect(X0 + 1, by + 68, mw - 2, bh - 69, fill="#EEF3F5", name="map water bg")
    m.draw_base(s)
    m.draw_programme(s, "adoption")
    with s.g("adoption legend"):
        lx = X0 + mw - 128
        s.text(lx, by + 96, "Farmers", 12, 600, INK2)
        for i, (lab, op) in enumerate([("2,000+", 0.95), ("1,500", 0.7), ("1,000", 0.5), ("< 800", 0.3)]):
            s.rect(lx, by + 110 + i * 26, 18, 16, fill=GREEN, op=op, rx=3)
            s.text(lx + 26, by + 123 + i * 26, lab, 12, 400, INK2)
        s.text(lx, by + 238, "Top: Mbarara", 12, 600, INK)
        s.text(lx, by + 256, "2,480 farmers", 12, 400, MUTED)
        s.text(lx, by + 290, "Open map →", 13, 600, GREEN)

    s.link(X0, by, mw, bh, "w09")
    tx = X0 + mw + 20
    tw_ = 600
    s.link(tx, by, tw_, bh, "w04")
    s.link(tx + tw_ + 20, by, X1 - tx - tw_ - 20, bh, "w06")
    card(s, tx, by, tw_, bh, "Partner reporting · Q3 2026", "Due 30 Sep · technical and financial reports",
         action="Open →")
    cols = [("Partner", 170, "start"), ("Technical", 150, "start"), ("Financial", 150, "start"),
            ("Evidence", 128, "end")]
    rows = []
    for p, t, f, (e1, e2), *_ in PARTNER_STATUS:
        rows.append([p, (lambda st: lambda s_, x, y, w, h: status_chip(s_, x + 12, y + h / 2 - 11, st, h=22, size=11))(t),
                     (lambda st: lambda s_, x, y, w, h: status_chip(s_, x + 12, y + h / 2 - 11, st, h=22, size=11))(f),
                     f"{e1}/{e2}"])
    table(s, tx + 1, by + 70, cols, rows, row_h=(bh - 72 - 34) / 8, head_h=32, size=13)

    ox = tx + tw_ + 20
    ow = X1 - ox
    card(s, ox, by, ow, bh, "Approved outcomes by signal", "Split by pathway · 64 outcomes")
    with s.g("pathway legend"):
        lx = ox + 24
        for p, c in PATHWAY.items():
            s.rect(lx, by + 76, 12, 12, fill=c, rx=3)
            lx += s.text(lx + 18, by + 87, p, 11.5, 600, INK2) + 34
    data = [(4, 3, 1), (2, 7, 1), (1, 1, 6), (0, 3, 3), (3, 5, 2), (1, 5, 1), (5, 3, 1), (2, 2, 3)]
    with s.g("stacked bars"):
        y = by + 108
        mxv = 12
        bw_ = ow - 24 - 64 - 40
        rh = (bh - 118) / 8
        for (code, lbl), vals in zip(SIGNALS, data):
            s.text(ox + 24, y + rh / 2 + 4, code, 12, 700, INK, name=code)
            x = ox + 64
            for v, c in zip(vals, (LEARN, LINK, LEVERAGE)):
                if v:
                    s.rect(x, y + rh / 2 - 8, bw_ * v / mxv - 2, 16, fill=c, rx=3)
                    x += bw_ * v / mxv
            s.text(x + 8, y + rh / 2 + 4, str(sum(vals)), 12, 600, INK2, name="total")
            y += rh
    return s


# =====================================================================================
def w03_indicator():
    s = shell("03 Indicator detail", "Indicators", ["Programme", "Indicators", "PHI 8 · Farmers adopting RA-PURE"])
    # ---- list panel
    lx, ly, lw = X0, Y0, 380
    with s.g("indicator list"):
        s.rect(lx, ly, lw, H - 28 - ly, fill=CARD, rx=12, stroke=LINE, name="bg")
        s.text(lx + 20, ly + 36, "Indicators", 17, 600, INK)
        s.text(lx + lw - 20, ly + 36, "24", 13, 600, MUTED, anchor="end")
        s.rect(lx + 16, ly + 52, lw - 32, 38, fill="#F4F6F3", rx=8, stroke=LINE)
        s.icon("search", lx + 28, ly + 62, 18, MUTED)
        s.text(lx + 54, ly + 76, "Search by name, code or signal", 13, 400, FAINT)
        x = lx + 16
        for t, on in [("All", True), ("Output", False), ("PHI", False), ("GESI", False)]:
            x += chip(s, x, ly + 102, t, GREEN if on else MUTED, h=26, size=12, solid=on) + 8
        groups = [("PATHWAY · LEARN", LEARN, [("OI 3.1", "People trained on RA-PURE", 0.62, GREEN),
                                             ("OI 3.2", "Learning events & exchanges held", 0.71, GREEN)]),
                  ("PATHWAY · LINK", LINK, [("PHI 8", "Farmers adopting RA-PURE practices", 0.41, AMBER),
                                            ("OI 2.1", "Agribusinesses using PURE solutions", 0.52, GREEN),
                                            ("OI 2.3", "Solar irrigation & processing units", 0.46, GREEN),
                                            ("OI 3.4", "Multi-actor platforms active", 0.58, GREEN)]),
                  ("PATHWAY · LEVERAGE", LEVERAGE, [("OI 4.1", "Policy engagements with evidence", 0.33, AMBER),
                                                    ("OI 4.2", "Finance mobilised for RA-PURE", 0.38, AMBER),
                                                    ("OI 4.3", "Partner organisational capacity score", 0.6, GREEN)])]
        y = ly + 150
        for gname, gcol, items in groups:
            s.text(lx + 20, y + 10, gname, 10.5, 600, gcol, spacing=0.8, name=gname)
            y += 22
            for code, name, fr, col in items:
                on = code == "PHI 8"
                with s.g(f"item {code}"):
                    if on:
                        s.rect(lx + 8, y - 4, lw - 16, 62, fill=tint(GREEN, 0.08), rx=8, stroke=tint(GREEN, 0.4))
                    s.text(lx + 20, y + 16, code, 12, 700, INK2)
                    s.text(lx + 72, y + 16, name, 13.5, 600 if on else 400, INK, maxw=lw - 100)
                    progress(s, lx + 72, y + 30, lw - 160, fr, col, h=6)
                    s.text(lx + lw - 20, y + 37, f"{round(fr * 100)}%", 12, 600, INK2, anchor="end")
                y += 64
            y += 8

    # ---- detail header
    dx = lx + lw + 20
    dw = X1 - dx
    with s.g("indicator header"):
        s.rect(dx, Y0, dw, 128, fill=CARD, rx=12, stroke=LINE)
        x = dx + 24
        for t, c in [("PHI 8", GREEN), ("SS5 · RA-PURE adoption", LINK), ("LINK", LINK), ("Quarterly", MUTED)]:
            x += chip(s, x, Y0 + 20, t, c, h=24, size=12) + 8
        s.text(dx + 24, Y0 + 72, "Farmers adopting RA-PURE innovations and practices", 24, 700, INK)
        para(s, dx + 24, Y0 + 97, "Number of smallholder farmers who adopted at least one regenerative practice "
                                  "powered by renewable energy, verified by partner adoption registers.", dw - 540,
             13, 400, MUTED, lh=19)
        bx = dx + dw - 24
        bx -= button(s, bx, Y0 + 18, "Export", "secondary", icon="download", anchor="end", h=36) + 10
        button(s, bx, Y0 + 18, "Edit definition", "secondary", icon="edit", anchor="end", h=36)
        with s.g("big numbers"):
            nx = dx + dw - 460
            for lab, val, sub, col in [("Achieved", "18,420", "approved", INK), ("Target 2029", "45,000", "", MUTED),
                                       ("Progress", "41%", "behind by 4 pts", AMBER_D)]:
                s.text(nx, Y0 + 80, lab.upper(), 10.5, 600, MUTED, spacing=0.8)
                s.text(nx, Y0 + 108, val, 24, 700, col if lab == "Progress" else INK)
                nx += 150

    # ---- tabs
    with s.g("tabs"):
        tx = dx + 4
        for t, on in [("Progress", True), ("Disaggregation", False), ("Submissions (8)", False),
                      ("Data dictionary", False), ("LogAlto mapping", False), ("History", False)]:
            wdt = tw(t, 14, 600)
            s.text(tx, Y0 + 162, t, 14, 600 if on else 400, GREEN if on else INK2)
            if on:
                s.rect(tx, Y0 + 172, wdt, 3, fill=GREEN, rx=1.5)
            tx += wdt + 32
        s.line(dx, Y0 + 175, X1, Y0 + 175, LINE)

    # ---- chart
    cy0 = Y0 + 195
    cwid = dw - 420 - 20
    card(s, dx, cy0, cwid, 380, "Cumulative progress vs target", "Approved values only · pending values shown hollow")
    with s.g("seg control"):
        sx = dx + cwid - 24 - 250
        s.rect(sx, cy0 + 20, 250, 34, fill="#F1F4F0", rx=8)
        s.rect(sx + 3, cy0 + 23, 120, 28, fill=CARD, rx=6, stroke=LINE)
        s.text(sx + 63, cy0 + 42, "Cumulative", 13, 600, INK, anchor="middle")
        s.text(sx + 186, cy0 + 42, "Per quarter", 13, 400, MUTED, anchor="middle")
    xl = ["Q1 25", "Q2 25", "Q3 25", "Q4 25", "Q1 26", "Q2 26", "Q3 26", "Q4 26"]
    line_chart(s, dx + 16, cy0 + 90, cwid - 48, 224, [
        ([4500, 9000, 13500, 18000, 22500, 27000, 31500, 36000], "#9AA59F", "Target", False),
        ([1200, 3900, 7400, 10500, 13600, 16110, 18420, None], GREEN, "Achieved", True),
    ], xl, 40000, 10000, fmt=lambda v: f"{v / 1000:.0f}k" if v else "0")
    with s.g("pending point"):
        px = dx + 16 + 44 + (cwid - 48 - 44) * 7.5 / 8
        py = cy0 + 90 + 224 - 224 * 19440 / 40000
        s.circle(px, py, 5, fill=CARD, stroke=GREEN, sw=2)
        s.line(px - 106, cy0 + 90 + 224 - 224 * 18420 / 40000, px, py, GREEN, 1.6, dash="4 4")
        s.rect(px - 150, py - 58, 164, 44, fill=INK, rx=8)
        s.text(px - 138, py - 38, "+1,020 pending review", 12, 600, "#FFFFFF")
        s.text(px - 138, py - 22, "NREP · not yet counted", 11.5, 400, "#C9D2CC")
    with s.g("chart legend"):
        lx2 = dx + 24
        s.rect(lx2, cy0 + 356, 14, 4, fill=GREEN, rx=2)
        s.text(lx2 + 20, cy0 + 362, "Achieved (approved)", 12, 400, INK2)
        s.line(lx2 + 170, cy0 + 358, lx2 + 190, cy0 + 358, "#9AA59F", 2, dash="5 4")
        s.text(lx2 + 196, cy0 + 362, "Target trajectory", 12, 400, INK2)

    # ---- data dictionary card
    ddx = dx + cwid + 20
    card(s, ddx, cy0, 420, 380, "How this indicator is counted", "Data dictionary · agreed with SNV MEL")
    rows = [("Unit", "Farmers (unique individuals)"), ("Calculation", "Count of unique farmers; cumulative"),
            ("Source", "Partner adoption register (app)"), ("Frequency", "Quarterly · partner → SNV"),
            ("Disaggregate", "Sex, age group, district, value chain"),
            ("Evidence", "Register with GPS + photo sample"), ("Validation", "Duplicate check on phone + name + village"),
            ("LogAlto", "Mapped → SNV-AGR-03 (push nightly)")]
    y = cy0 + 94
    for k, v in rows:
        s.text(ddx + 24, y, k, 12.5, 600, MUTED, name=k)
        s.text(ddx + 130, y, v, 13, 400, INK, maxw=270, name="value")
        s.line(ddx + 24, y + 13, ddx + 396, y + 13, LINE2)
        y += 34

    # ---- disaggregation + submissions
    by = cy0 + 400
    bh = H - 28 - by
    dw1 = 560
    card(s, dx, by, dw1, bh, "Who is adopting", "GESI disaggregation · approved values")
    donut(s, dx + 110, by + 170, 70, 22, [(54, "#9D4A8C", "Women"), (46, "#4A7FC1", "Men")], name="sex donut")
    s.text(dx + 110, by + 168, "54%", 22, 700, INK, anchor="middle")
    s.text(dx + 110, by + 188, "women", 12, 400, MUTED, anchor="middle")
    with s.g("age and value chain"):
        gx = dx + 220
        s.text(gx, by + 100, "Age group", 12.5, 600, MUTED)
        for i, (lab, v, c) in enumerate([("Youth 18–35", 0.38, AMBER), ("Adults 36+", 0.62, GREEN_M)]):
            s.text(gx, by + 128 + i * 30, lab, 13, 400, INK)
            progress(s, gx + 100, by + 120 + i * 30, 150, v, c, h=8)
            s.text(gx + 300, by + 128 + i * 30, f"{round(v * 100)}%", 12.5, 600, INK2, anchor="end")
        s.text(gx, by + 200, "Value chain", 12.5, 600, MUTED)
        for i, (lab, v) in enumerate([("Coffee", 0.31), ("Dairy", 0.24), ("Horticulture", 0.22), ("Grains", 0.23)]):
            s.text(gx, by + 228 + i * 28, lab, 13, 400, INK)
            progress(s, gx + 100, by + 220 + i * 28, 150, v / 0.35, GREEN, h=8)
            s.text(gx + 300, by + 228 + i * 28, f"{round(v * 100)}%", 12.5, 600, INK2, anchor="end")

    sx = dx + dw1 + 20
    sw_ = X1 - sx
    card(s, sx, by, sw_, bh, "Submissions this period", "Only Approved rows count towards the figure above",
         action="Review 2 →")
    cols = [("Partner", 130, "start"), ("District(s)", 180, "start"), ("Value", 76, "end"), ("Evidence", 104, "start"),
            ("Status", sw_ - 490 - 2, "start")]

    def ev(n, ok=True):
        def f(s_, x, y, w, h):
            s_.icon("clip", x + 16, y + h / 2 - 8, 16, STATUS["Approved"] if ok else STATUS["Returned"], 2)
            s_.text(x + 38, y + h / 2 + 4.5, n, 13, 400, INK if ok else STATUS["Returned"])
        return f

    def st(v):
        return lambda s_, x, y, w, h: status_chip(s_, x + 16, y + h / 2 - 11, v, h=22, size=11)

    rows = [["NOGAMU", "Masaka, Mpigi, Luwero", "3,120", ev("4 files"), st("Approved")],
            ["NREP", "Mbarara, Isingiro, Lira", "1,020", ev("3 files"), st("Under review")],
            ["PELUM Uganda", "Mubende, Kasese", "1,480", ev("5 files"), st("Approved")],
            ["CREEC", "Mbale, Jinja", "410", ev("missing", False), st("Returned")],
            ["USEA", "Masaka, Lira", "—", ev("—", False), st("Overdue")]]
    table(s, sx + 1, by + 72, cols, rows, row_h=(bh - 74 - 36) / 5, head_h=36)
    return s


# =====================================================================================
def w04_partner_reporting():
    s = shell("04 Partner reporting compliance (SNV)", "Partner reporting", ["Partners", "Partner reporting"])
    page_head(s, "Partner reporting · Q3 2026", "Quarterly technical and financial reports from the eight implementing "
                                                "partners — due 30 September 2026 (6 days left)")
    x = X1
    x -= button(s, x, Y0 + 12, "Export compliance summary", "secondary", icon="download", anchor="end") + 12
    button(s, x, Y0 + 12, "Send reminder to 2 partners", "primary", icon="send", anchor="end")

    ty = Y0 + 84
    tiles = [("Approved", "5", "reports", STATUS["Approved"]), ("Under review", "4", "with SNV MEL", STATUS["Under review"]),
             ("Submitted", "2", "awaiting pickup", STATUS["Submitted"]), ("Returned", "1", "for revision", STATUS["Returned"]),
             ("Overdue", "2", "USEA · both reports", STATUS["Overdue"]), ("Missing evidence", "13", "of 83 items", "#6D5BD0")]
    tw_ = (CW - 5 * 16) / 6
    for i, (lab, val, sub, col) in enumerate(tiles):
        x = X0 + i * (tw_ + 16)
        with s.g(f"tile {lab}"):
            s.rect(x, ty, tw_, 96, fill=CARD, rx=12, stroke=LINE)
            s.rect(x, ty + 16, 4, 64, fill=col, rx=2)
            s.text(x + 22, ty + 32, lab, 13, 600, INK2)
            s.text(x + 22, ty + 70, val, 30, 700, INK)
            s.text(x + 30 + tw(val, 30, 700), ty + 70, sub, 12.5, 400, MUTED)

    cy = ty + 116
    ch = 564
    card(s, X0, cy, CW, ch, "Compliance by partner", "Partners only ever see their own row · financial detail is "
                                                     "restricted to SNV finance and MEL", action="View Q2 2026 →")
    cols = [("Partner", 250, "start"), ("MEL focal person", 210, "start"), ("Technical report", 190, "start"),
            ("Financial report", 190, "start"), ("Evidence", 170, "start"), ("Workplan activities", 260, "start"),
            ("Sub-grant disbursed", 190, "start"), ("", CW - 1460 - 2, "end")]
    partner_col = {"ACSA": "#2E8B57", "PELUM Uganda": "#8E5BD6", "NREP": "#E0911A", "ACME": "#C2362F",
                   "CREEC": "#2B6CB0", "NOGAMU": "#178A4C", "NARO": "#0F766E", "USEA": "#B7791F"}
    disb = {"ACSA": 0.7, "PELUM Uganda": 0.62, "NREP": 0.66, "ACME": 0.75, "CREEC": 0.5, "NOGAMU": 0.7, "NARO": 0.45,
            "USEA": 0.33}
    rows = []
    for p, t, f, (e1, e2), wp, focal, last in PARTNER_STATUS:
        def pcell(s_, x, y, w, h, p=p):
            ini = "".join(w_[0] for w_ in p.split())[:2] if " " in p else p[:2]
            s_.rect(x + 16, y + h / 2 - 16, 32, 32, fill=tint(partner_col[p], 0.15), rx=8)
            s_.text(x + 32, y + h / 2 + 4.5, ini.upper(), 12, 700, shade(partner_col[p], 0.1), anchor="middle")
            s_.text(x + 58, y + h / 2 + 5, p, 14, 600, INK)

        def fcell(s_, x, y, w, h, focal=focal, last=last):
            s_.text(x + 16, y + h / 2 - 2, focal, 13.5, 400, INK)
            s_.text(x + 16, y + h / 2 + 16, f"Last activity {last}", 12, 400, MUTED)

        def stc(v):
            def f_(s_, x, y, w, h):
                status_chip(s_, x + 16, y + h / 2 - 12, v)
            return f_

        def ecell(s_, x, y, w, h, e1=e1, e2=e2):
            ok = e1 == e2
            col = STATUS["Approved"] if ok else (STATUS["Overdue"] if e1 == 0 else STATUS["Returned"])
            s_.icon("check" if ok else "alert", x + 16, y + h / 2 - 8, 16, col, 2.2)
            s_.text(x + 38, y + h / 2 + 5, f"{e1} of {e2}", 13.5, 600, INK)
            if not ok:
                s_.text(x + 38 + tw(f"{e1} of {e2}", 13.5, 600) + 6, y + h / 2 + 5, "missing", 12, 400, col)

        def wcell(s_, x, y, w, h, wp=wp):
            progress(s_, x + 16, y + h / 2 - 4, 150, wp, GREEN if wp > 0.55 else AMBER, h=8)
            s_.text(x + 176, y + h / 2 + 4, f"{round(wp * 26)}/26", 12.5, 600, INK2)

        def dcell(s_, x, y, w, h, p=p):
            v = disb[p]
            s_.icon("lock", x + 16, y + h / 2 - 8, 15, MUTED, 2)
            s_.text(x + 38, y + h / 2 + 5, f"{round(v * 100)}% of tranche", 13, 400, INK)

        def acell(s_, x, y, w, h, t=t):
            label = "Remind" if t == "Overdue" else ("Review" if t in ("Submitted", "Under review") else "Open")
            button(s_, x + w - 16, y + h / 2 - 16, label, "primary" if label == "Review" else "secondary", h=32,
                   size=13, anchor="end")

        rows.append([pcell, fcell, stc(t), stc(f), ecell, wcell, dcell, acell])
    table(s, X0 + 1, cy + 80, cols, rows, row_h=55, head_h=40, hl=7)
    s.link(X0, cy + 120 + 2 * 55, CW, 55, "w05")
    s.link(X0, cy + 120 + 6 * 55, CW, 55, "w05")

    fy = cy + ch + 20
    fh = H - 28 - fy
    fw = (CW - 20) * 0.6
    card(s, X0, fy, fw, fh, "Follow-up actions", None)
    items = [("alert", STATUS["Overdue"], "USEA — Q3 technical & financial reports overdue", "Auto-reminder sent 23 Sep · escalate to Programme Manager"),
             ("clip", STATUS["Returned"], "CREEC — returned: 3 evidence files missing for OI 2.3", "Returned 20 Sep by Grace Akello · partner notified by email and SMS")]
    y = fy + 64
    for ic, col, t1, t2 in items:
        s.rect(X0 + 24, y, 30, 30, fill=tint(col, 0.12), rx=8)
        s.icon(ic, X0 + 31, y + 7, 16, col, 2)
        s.text(X0 + 66, y + 13, t1, 13.5, 600, INK)
        s.text(X0 + 66, y + 31, t2, 12.5, 400, MUTED)
        y += 46
    rx = X0 + fw + 20
    card(s, rx, fy, CW - fw - 20, fh, "Automatic reminders", None)
    y = fy + 76
    for t, on in [("7 days before due date · email + SMS", True), ("On due date · email + in-app", True),
                  ("3 days overdue · copy Programme Manager", True)]:
        toggle(s, rx + 24, y - 14, on)
        s.text(rx + 72, y + 1, t, 13, 400, INK2)
        y += 32
    return s


# =====================================================================================
def w05_report_review():
    s = shell("05 Report review (SNV MEL)", "Review queue", ["Partners", "Review queue", "NREP · Q3 2026 technical report"])
    # header
    with s.g("report header"):
        s.text(X0, Y0 + 30, "NREP · Q3 2026 technical report", 26, 700, INK)
        x = X0
        y = Y0 + 44
        x += status_chip(s, x, y, "Under review") + 8
        x += chip(s, x, y, "Version 2 · resubmitted 18 Sep", MUTED) + 8
        chip(s, x, y, "Submitted by Brian Tumusiime", MUTED, icon="user")
        bx = X1
        bx -= button(s, bx, Y0 + 12, "Compare with v1", "secondary", icon="copy", anchor="end") + 10
        button(s, bx, Y0 + 12, "Download PDF", "secondary", icon="download", anchor="end")

    lw = 1030
    ly = Y0 + 90
    # section tabs
    with s.g("report sections"):
        tx = X0
        for t, on, flag in [("Indicator results", True, "1"), ("Activities & workplan", False, None),
                            ("Outcomes (2)", False, None), ("Narrative", False, None), ("Evidence (12)", False, "1")]:
            w_ = tw(t, 14, 600)
            s.text(tx, ly + 20, t, 14, 600 if on else 400, GREEN if on else INK2)
            if flag:
                s.circle(tx + w_ + 16, ly + 15, 8, fill=STATUS["Returned"])
                s.text(tx + w_ + 16, ly + 19, flag, 10, 700, "#FFFFFF", anchor="middle")
            if on:
                s.rect(tx, ly + 30, w_, 3, fill=GREEN, rx=1.5)
            tx += w_ + (48 if flag else 32)
        s.line(X0, ly + 33, X0 + lw, ly + 33, LINE)

    cy = ly + 52
    ch = H - 28 - cy
    card(s, X0, cy, lw, ch, "Indicator results reported", "Figures NREP entered for this quarter, with the checks the "
                                                           "system ran on submission")
    cols = [("Indicator", 330, "start"), ("This quarter", 120, "end"), ("Last quarter", 120, "end"),
            ("Evidence", 150, "start"), ("System checks", lw - 720 - 2, "start")]

    def evc(n, ok=True):
        def f(s_, x, y, w, h):
            s_.icon("clip", x + 16, y + h / 2 - 8, 16, GREEN if ok else STATUS["Returned"], 2)
            s_.text(x + 38, y + h / 2 + 5, n, 13, 600 if ok else 400, GREEN if ok else STATUS["Returned"])
        return f

    def chk(kind, text):
        col = {"ok": STATUS["Approved"], "warn": STATUS["Under review"], "err": STATUS["Returned"]}[kind]
        ic = {"ok": "check", "warn": "alert", "err": "alert"}[kind]

        def f(s_, x, y, w, h):
            s_.icon(ic, x + 16, y + h / 2 - 8, 16, col, 2.2)
            s_.text(x + 40, y + h / 2 + 5, text, 13, 400, INK if kind == "ok" else shade(col, 0.1), maxw=w - 56)
        return f

    def ind(code, name):
        def f(s_, x, y, w, h):
            s_.text(x + 16, y + h / 2 - 3, name, 13.5, 600, INK, maxw=w - 28)
            s_.text(x + 16, y + h / 2 + 15, code, 12, 400, MUTED)
        return f

    rows = [
        [ind("PHI 8 · SS5", "Farmers adopting RA-PURE practices"), "1,020", "620", evc("3 files"),
         chk("warn", "65% above last quarter · explained")],
        [ind("OI 2.1", "Agribusinesses using PURE solutions"), "18", "14", evc("2 files"), chk("ok", "Within expected range")],
        [ind("OI 2.3", "Solar irrigation & processing units"), "74", "52", evc("4 files"),
         chk("ok", "GPS on 74 of 74 installations")],
        [ind("OI 3.1", "People trained on RA-PURE"), "640", "590", evc("2 files"), chk("ok", "Attendance lists match total")],
        [ind("OI 3.4", "Multi-actor platforms active"), "3", "3", evc("0 files", False),
         chk("err", "Evidence required — meeting minutes")],
        [ind("OI 4.1", "Policy engagements with evidence"), "2", "1", evc("1 file"), chk("ok", "Linked to outcome OH-041")],
    ]
    ry = table(s, X0 + 1, cy + 80, cols, rows, row_h=64, head_h=40, hl=0)
    with s.g("explanation box"):
        by = ry + 18
        s.rect(X0 + 24, by, lw - 48, 120, fill=tint(STATUS["Under review"], 0.08), rx=10,
               stroke=tint(STATUS["Under review"], 0.35))
        s.icon("message", X0 + 42, by + 18, 18, AMBER_D, 2)
        s.text(X0 + 70, by + 32, "Partner explanation for PHI 8 jump", 13.5, 600, INK)
        para(s, X0 + 70, by + 56, "“Two new solar-irrigation clusters in Isingiro (Kabingo and Masha sub-counties) "
                                  "reached farmers trained in Q2. The adoption register lists all 1,020 farmers with "
                                  "phone, village and GPS.”", lw - 140, 13, 400, INK2, lh=21)
    with s.g("version history"):
        hy = by + 150
        s.text(X0 + 24, hy, "Version history", 13.5, 600, INK)
        steps = [("Draft", "12 Sep", "Draft"), ("Submitted", "15 Sep", "Submitted"), ("Returned", "16 Sep", "Returned"),
                 ("Resubmitted · v2", "18 Sep", "Submitted"), ("Under review", "Now", "Under review"),
                 ("Approved", "—", "Not due")]
        sw_ = (lw - 48) / len(steps)
        for i, (lab, d, st) in enumerate(steps):
            cx = X0 + 24 + i * sw_ + 10
            col = STATUS[st]
            if i < len(steps) - 1:
                s.line(cx + 10, hy + 32, cx + sw_, hy + 32, LINE if i >= 4 else tint(GREEN, 0.5), 2,
                       dash="4 4" if i >= 4 else None)
            s.circle(cx, hy + 32, 9, fill=col if i <= 4 else CARD, stroke=col, sw=2)
            s.text(cx - 10, hy + 64, lab, 12.5, 600, INK if i <= 4 else MUTED)
            s.text(cx - 10, hy + 82, d, 12, 400, MUTED)

    # ---- review panel
    px = X0 + lw + 24
    pw = X1 - px
    py = Y0 + 90
    ph = H - 28 - py
    with s.g("review panel"):
        s.rect(px, py, pw, ph, fill=CARD, rx=12, stroke=LINE, name="panel bg")
        s.text(px + 24, py + 38, "Your review", 17, 600, INK)
        s.text(px + 24, py + 60, "Checks run automatically when the partner submits", 13, 400, MUTED)
        y = py + 84
        checks = [("check", STATUS["Approved"], "Mandatory fields complete", "42 of 42"),
                  ("check", STATUS["Approved"], "No duplicate farmers found", "checked against all partners"),
                  ("alert", STATUS["Under review"], "1 value outside expected range", "PHI 8 · explained"),
                  ("alert", STATUS["Returned"], "1 result has no evidence", "OI 3.4 · minutes needed")]
        for ic, col, t1, t2 in checks:
            s.rect(px + 24, y, pw - 48, 50, fill="#F8FAF7", rx=8)
            s.icon(ic, px + 38, y + 16, 18, col, 2.2)
            s.text(px + 66, y + 22, t1, 13.5, 600, INK)
            s.text(px + 66, y + 40, t2, 12, 400, MUTED)
            y += 58
        # comments
        y += 10
        s.text(px + 24, y + 14, "Conversation", 14, 600, INK)
        y += 30
        for who, ini, col, when, msg in [
            ("Grace Akello", "GA", GREEN, "20 Sep", "Please attach the Isingiro adoption register for PHI 8 and the "
                                                   "platform meeting minutes for OI 3.4."),
            ("Brian Tumusiime", "BT", LEARN, "18 Sep", "Register attached. Minutes are being signed by the district "
                                                       "chair — will upload by Friday.")]:
            avatar(s, px + 40, y + 16, 16, ini, col)
            s.text(px + 64, y + 12, who, 13, 600, INK)
            s.text(px + 68 + tw(who, 13, 600), y + 12, "· " + when, 12, 400, MUTED)
            h_ = para(s, px + 64, y + 32, msg, pw - 100, 13, 400, INK2, lh=19)
            y += 32 + h_ + 10
        s.rect(px + 24, y, pw - 48, 76, fill=CARD, rx=8, stroke="#CFD6D1", name="comment box")
        s.text(px + 38, y + 26, "Write feedback for NREP…", 13, 400, FAINT)
        s.icon("clip", px + pw - 60, y + 48, 18, MUTED)
        y += 92
        # decision
        with s.g("decision"):
            s.text(px + 24, y + 14, "Decision", 14, 600, INK)
            y += 28
            bw = (pw - 48 - 12) / 2
            button(s, px + 24, y, "Return for revision", "danger", icon="arrowleft", w=bw, h=44)
            button(s, px + 36 + bw, y, "Approve 5 of 6 results", "primary", icon="check", w=bw, h=44)
            s.link(px + 24, y, pw - 48, 44, "w04")
            y += 58
            s.rect(px + 24, y, pw - 48, 58, fill=tint(GREEN, 0.07), rx=8)
            s.icon("shield", px + 38, y + 11, 18, GREEN, 2)
            para(s, px + 66, y + 24, "Approved results go into dashboards, donor extracts and the next LogAlto push. "
                                     "Every decision is written to the audit trail.", pw - 110, 12, 400, INK2, lh=18)
    return s


# =====================================================================================
OUTCOMES = {
    "Draft": [("Kasese radio station runs a weekly call-in show on regenerative farming", "ACME", ["SS1"], "LEARN", "Kasese", 1, "22 Sep"),
              ("Nakasongola cattle keepers pooled funds for a shared solar water pump", "ACSA", ["SS5", "SS4"], "LINK", "Nakasongola", 0, "23 Sep"),
              ("Mubende district agreed to include soil health in its production plan", "PELUM Uganda", ["SS3"], "LEVERAGE", "Mubende", 1, "23 Sep")],
    "Submitted": [
        ("Five SACCOs in Masaka began offering asset loans for solar dryers to coffee farmers", "USEA", ["SS4", "SS6"], "LINK", "Masaka", 3, "21 Sep"),
        ("Lira farmer groups formed a joint RA-PURE learning platform with NARO researchers", "NARO", ["SS2"], "LEARN", "Lira", 2, "19 Sep"),
        ("Solar pump dealers in Luwero introduced pay-as-you-go packages for farmer groups", "NOGAMU", ["SS6", "SS4"], "LINK", "Luwero", 4, "17 Sep")],
    "Under review": [
        ("Mbarara District allocated UGX 120M in its FY26/27 budget for solar irrigation demonstration sites", "NREP", ["SS3", "SS4"], "LEVERAGE", "Mbarara", 5, "16 Sep"),
        ("Women-led agro-processors in Mbale negotiated shared access to a solar maize mill", "CREEC", ["SS8", "SS6"], "LINK", "Mbale", 3, "14 Sep"),
        ("Kabarole agricultural extension officers adopted the RA training curriculum", "PELUM Uganda", ["SS7"], "LEVERAGE", "Kabarole", 2, "12 Sep")],
    "Returned": [
        ("Isingiro dairy cooperative adopted solar milk chilling, cutting spoilage losses", "NREP", ["SS5", "SS6"], "LINK", "Isingiro", 1, "10 Sep"),
        ("Iganga traders began buying sun-dried cassava chips at a premium", "CREEC", ["SS6"], "LINK", "Iganga", 1, "08 Sep")],
    "Approved": [
        ("MEMD included productive use of solar in agriculture in the draft energy policy review", "NREP", ["SS3"], "LEVERAGE", "National", 6, "02 Sep"),
        ("Kayunga extension workers now test soil health on routine farm visits", "NOGAMU", ["SS7", "SS1"], "LEARN", "Kayunga", 4, "28 Aug"),
        ("Jinja youth groups set up a solar cold-room enterprise for horticulture", "CREEC", ["SS5", "SS8"], "LINK", "Jinja", 3, "21 Aug")],
}
COUNTS = {"Draft": 3, "Submitted": 5, "Under review": 4, "Returned": 2, "Approved": 64}


def outcome_card(s: SVG, x, y, w, oc, status, selected=False):
    title, partner, sigs, pw, district, ev, date = oc
    lines = wrap(title, w - 32, 13.5, 600)[:3]
    h = 126 + 20 * len(lines)
    with s.g(f"outcome card {title[:24]}"):
        s.rect(x, y, w, h, fill=CARD, rx=10, stroke=GREEN if selected else LINE, sw=2 if selected else 1)
        cx = x + 16
        cx += chip(s, cx, y + 14, pw, PATHWAY[pw], h=22, size=11) + 6
        for sg in sigs:
            cx += chip(s, cx, y + 14, sg, "#5B6770", h=22, size=11) + 6
        for i, ln in enumerate(lines):
            s.text(x + 16, y + 60 + i * 20, ln, 13.5, 600, INK, name="title line")
        yy = y + 60 + 20 * len(lines) + 4
        s.line(x + 16, yy, x + w - 16, yy, LINE2)
        s.text(x + 16, yy + 24, partner, 12.5, 600, INK2, name="partner")
        s.icon("pin", x + 20 + tw(partner, 12.5, 600), yy + 12, 14, MUTED, 2)
        s.text(x + 38 + tw(partner, 12.5, 600), yy + 24, district, 12.5, 400, MUTED, name="district")
        s.icon("clip", x + 16, yy + 36, 14, MUTED, 2)
        s.text(x + 34, yy + 48, f"{ev} evidence", 12, 400, MUTED)
        s.text(x + w - 16, yy + 48, date, 12, 400, MUTED, anchor="end")
    return h


def w06_outcome_board():
    s = shell("06 Outcome harvesting board", "Outcome harvesting", ["Programme", "Outcome harvesting"])
    page_head(s, "Outcome harvesting", "Changes in the behaviour, relationships, policies and practices of system "
                                       "actors — harvested by partners, substantiated, and linked to SS1–SS8")
    x = X1
    x -= button(s, x, Y0 + 12, "Harvest an outcome", "primary", icon="plus", anchor="end") + 12
    x -= button(s, x, Y0 + 12, "Outcome harvesting log", "secondary", icon="download", anchor="end") + 12
    with s.g("view switch"):
        s.rect(x - 188, Y0 + 12, 188, 40, fill="#EDF1EC", rx=8)
        s.rect(x - 185, Y0 + 15, 90, 34, fill=CARD, rx=6, stroke=LINE)
        s.text(x - 140, Y0 + 37, "Board", 13, 600, INK, anchor="middle")
        s.text(x - 48, Y0 + 37, "Table", 13, 400, MUTED, anchor="middle")

    fy = Y0 + 80
    with s.g("filters"):
        s.rect(X0, fy, 320, 40, fill=CARD, rx=8, stroke=LINE)
        s.icon("search", X0 + 12, fy + 11, 18, MUTED)
        s.text(X0 + 40, fy + 25, "Search outcome statements", 13, 400, FAINT)
        fx = X0 + 336
        for lab, val in [("Partner", "All"), ("Signal", "All"), ("Pathway", "All"), ("District", "All"),
                         ("Actor", "All")]:
            fx += filter_btn(s, fx, fy + 1, lab, val) + 10
        s.text(X1, fy + 26, "79 outcomes this programme year", 13, 400, MUTED, anchor="end")

    cols = ["Draft", "Submitted", "Under review", "Returned", "Approved"]
    colw = (CW - 4 * 16) / 5
    top = fy + 60
    for i, st in enumerate(cols):
        x = X0 + i * (colw + 16)
        with s.g(f"column {st}"):
            s.rect(x, top, colw, H - 28 - top, fill="#EDF1EC", rx=12, name="column bg")
            s.circle(x + 20, top + 24, 5, fill=STATUS[st])
            s.text(x + 32, top + 29, st, 14, 600, INK)
            n = str(COUNTS[st])
            s.rect(x + 40 + tw(st, 14, 600), top + 15, tw(n, 12, 600) + 16, 20, fill=CARD, rx=10)
            s.text(x + 48 + tw(st, 14, 600), top + 29, n, 12, 600, INK2)
            s.icon("more", x + colw - 34, top + 14, 20, MUTED, 2.6)
            y = top + 48
            for oc in OUTCOMES[st]:
                h = outcome_card(s, x + 10, y, colw - 20, oc, st, selected=oc[1] == "NREP" and st == "Under review")
                s.link(x + 10, y, colw - 20, h, "w07")
                y += h + 10
            more = COUNTS[st] - len(OUTCOMES[st])
            if more > 0:
                s.text(x + colw / 2, y + 22, f"+ {more} more", 13, 600, GREEN, anchor="middle")
                y += 40
            if st == "Returned":
                with s.g("returned note"):
                    s.rect(x + 10, y, colw - 20, 72, fill=tint(STATUS["Returned"], 0.08), rx=10,
                           stroke=tint(STATUS["Returned"], 0.35), dash="4 3")
                    para(s, x + 24, y + 26, "Returned outcomes go back to the partner with SNV's note. The partner "
                                            "edits and resubmits; each version is kept.", colw - 48, 12, 400, INK2, lh=18)
    return s


# =====================================================================================
def w07_outcome_detail():
    s = shell("07 Outcome review & signal mapping", "Outcome harvesting",
              ["Programme", "Outcome harvesting", "OH-052"])
    with s.g("header"):
        x = X0
        x += chip(s, x, Y0 + 4, "OH-052", MUTED) + 8
        x += status_chip(s, x, Y0 + 4, "Under review") + 8
        chip(s, x, Y0 + 4, "Harvested by NREP · 16 Sep 2026", MUTED, icon="user")
        s.text(X0, Y0 + 62, "Mbarara District allocated UGX 120M in its FY26/27 budget for solar irrigation "
                            "demonstration sites", 24, 700, INK)
    lw = 1000
    y0 = Y0 + 90
    # outcome description card
    card(s, X0, y0, lw, 330, "The outcome, as harvested", "Outcome harvesting template · all fields mandatory")
    blocks = [("What changed, who changed it, when and where",
               "In August 2026 the Mbarara District Council approved a UGX 120 million line in its FY2026/27 budget to "
               "establish four solar-powered irrigation demonstration sites with farmer groups in Bubaare and "
               "Rubindi sub-counties. This is the first district budget allocation for PURE in agriculture in the region."),
              ("Why it matters (significance)",
               "Shows local government moving from hosting pilots to funding them — an early LEVERAGE signal that "
               "RA-PURE can be sustained through public budgets beyond the programme."),
              ("How the programme contributed",
               "NREP and USEA presented adoption and yield evidence at two district budget conferences and supported "
               "the production office to cost the sites.")]
    y = y0 + 90
    for h1, body in blocks:
        s.text(X0 + 24, y, h1, 13, 600, MUTED, name=h1[:20])
        y += 22
        y += para(s, X0 + 24, y, body, lw - 48, 14, 400, INK, lh=22) + 8

    # evidence
    ey = y0 + 350
    eh = H - 28 - ey
    card(s, X0, ey, lw, eh, "Evidence and substantiation", "Every approved outcome must link to at least one "
                                                          "verifiable source", action="+ Link evidence")
    ev = [("file", "District approved budget FY26/27 — extract p.14", "PDF · 1.2 MB · uploaded by NREP", "Verified"),
          ("image", "Budget conference photos — Mbarara, 14 Aug", "4 photos · GPS tagged · consent recorded", "Verified"),
          ("file", "Council minutes, 22 Aug 2026 (min. 6/2026)", "PDF · 480 KB", "Verified"),
          ("message", "Substantiation call — District Production Officer", "Note by Grace Akello · 19 Sep", "Pending"),
          ("link", "Linked indicator: OI 4.2 Finance mobilised for RA-PURE", "Adds UGX 120M (≈ €29k) once approved", "Linked")]
    y = ey + 80
    rowh = (eh - 92) / len(ev)
    for ic, t1, t2, st in ev:
        with s.g(f"evidence {t1[:20]}"):
            s.rect(X0 + 24, y + (rowh - 44) / 2, 44, 44, fill=tint(GREEN, 0.08), rx=8)
            s.icon(ic, X0 + 35, y + (rowh - 44) / 2 + 11, 22, GREEN, 1.8)
            s.text(X0 + 84, y + rowh / 2 - 3, t1, 14, 600, INK)
            s.text(X0 + 84, y + rowh / 2 + 16, t2, 12.5, 400, MUTED)
            col = {"Verified": STATUS["Approved"], "Pending": STATUS["Under review"], "Linked": LEARN}[st]
            chip(s, X0 + lw - 24 - tw(st, 12, 600) - 34, y + rowh / 2 - 12, st, col, dot=True)
            if ic != "link":
                s.line(X0 + 84, y + rowh, X0 + lw - 24, y + rowh, LINE2)
        y += rowh

    # ---- categorise panel
    px = X0 + lw + 24
    pw = X1 - px
    ph = H - 28 - y0
    with s.g("categorise panel"):
        s.rect(px, y0, pw, ph, fill=CARD, rx=12, stroke=LINE, name="panel bg")
        s.text(px + 24, y0 + 38, "SNV categorisation", 17, 600, INK)
        s.text(px + 24, y0 + 60, "How this outcome will be counted and aggregated", 13, 400, MUTED)
        y = y0 + 92
        s.text(px + 24, y, "System Signals", 13, 600, INK2)
        s.text(px + pw - 24, y, "choose all that apply", 12, 400, MUTED, anchor="end")
        y += 14
        colw = (pw - 48 - 12) / 2
        for i, (code, name) in enumerate(SIGNALS):
            cx = px + 24 + (i % 2) * (colw + 12)
            cy = y + (i // 2) * 44
            on = code in ("SS3", "SS4")
            with s.g(f"signal {code}"):
                s.rect(cx, cy, colw, 36, fill=tint(LINK, 0.08) if on else CARD, rx=8,
                       stroke=tint(LINK, 0.6) if on else LINE)
                checkbox(s, cx + 10, cy + 9, on, color=LINK)
                s.text(cx + 36, cy + 23, code, 12.5, 700, INK)
                s.text(cx + 70, cy + 23, name, 12.5, 400, INK2, maxw=colw - 80)
        y += 4 * 44 + 18
        s.text(px + 24, y, "Pathway", 13, 600, INK2)
        y += 14
        pwid = (pw - 48 - 16) / 3
        for i, p in enumerate(PATHWAY):
            on = p == "LEVERAGE"
            cx = px + 24 + i * (pwid + 8)
            s.rect(cx, y, pwid, 38, fill=tint(PATHWAY[p], 0.1) if on else CARD, rx=8,
                   stroke=PATHWAY[p] if on else LINE, sw=1.5 if on else 1, name=f"pathway {p}")
            radio(s, cx + 20, y + 19, on, 8, PATHWAY[p])
            s.text(cx + 36, y + 24, p, 13, 600, INK)
        y += 60
        fw = (pw - 48 - 16) / 2
        field(s, px + 24, y, fw, "Actor category", "Local government", h=40, dropdown=True, size=13)
        field(s, px + 40 + fw, y, fw, "Transformation dimension", "Policy & public finance", h=40, dropdown=True, size=13)
        y += 78
        field(s, px + 24, y, fw, "Value chain", "Horticulture, Dairy", h=40, dropdown=True, size=13)
        field(s, px + 40 + fw, y, fw, "Geography", "Mbarara · 2 sub-counties", h=40, dropdown=True, size=13, icon="pin")
        y += 84
        s.text(px + 24, y, "Quality check", 13, 600, INK2)
        y += 10
        for ok, t in [(True, "Specific: who, what, when, where"), (True, "Plausible programme contribution"),
                      (True, "Verified by an independent source"), (False, "Substantiation call logged")]:
            checkbox(s, px + 24, y + 4, ok)
            s.text(px + 52, y + 18, t, 13, 400, INK if ok else MUTED)
            y += 28
        y = y0 + ph - 72
        s.line(px, y - 12, px + pw, y - 12, LINE)
        bw = (pw - 48 - 20) / 3
        button(s, px + 24, y, "Return", "danger", w=bw, h=44)
        button(s, px + 34 + bw, y, "Reject", "secondary", w=bw, h=44)
        button(s, px + 44 + 2 * bw, y, "Approve", "primary", icon="check", w=bw, h=44)
        s.link(px + 24, y, pw - 48, 44, "w06")
    return s


# =====================================================================================
RUBRIC = [
    (0, "No signal", "No observable change among system actors."),
    (1, "Emerging", "Isolated, one-off changes by individual actors, mostly driven by programme support."),
    (2, "Developing", "Several actors changing; some initiatives continue without programme support."),
    (3, "Established", "Changes repeated and spreading; actors investing their own resources."),
    (4, "Embedded", "Change is self-sustaining and institutionalised in policy, markets or norms."),
]


def w08_signals():
    s = shell("08 System Signal scoring (Sense Making)", "System Signals", ["Programme", "System Signals"])
    page_head(s, "System Signals · Sense Making", "Score each signal 0–4 against the rubric, with justification and "
                                                  "linked outcomes. Scores are compared across Pause & Reflect sessions.")
    x = X1
    x -= button(s, x, Y0 + 12, "Export radar (PNG / PDF)", "secondary", icon="download", anchor="end") + 12
    filter_btn(s, x - 330, Y0 + 13, "Session", "Pause & Reflect · 16 Sep 2026", w=330)

    lw = 860
    y0 = Y0 + 84
    ch = H - 28 - y0
    card(s, X0, y0, lw, ch, "Signals over time", "Programme-level scores agreed in session · 7 participants "
                                                 "(SNV, NREP, NOGAMU, PELUM, CREEC, USEA, NARO)")
    with s.g("legend"):
        lx = X0 + 24
        for lab, col, dash in [("Q3 2026 (this session)", GREEN, False), ("Q1 2026", LEARN, True),
                               ("Baseline Q4 2025", AMBER_D, True)]:
            if dash:
                s.line(lx, y0 + 96, lx + 22, y0 + 96, col, 2, dash="4 3")
            else:
                s.rect(lx, y0 + 89, 22, 14, fill=col, op=0.3, stroke=col)
            lx += s.text(lx + 30, y0 + 101, lab, 12.5, 400, INK2) + 58
    radar(s, X0 + lw / 2, y0 + 345, 188, [
        ([1.5, 2.0, 1.0, 1.0, 1.5, 1.5, 2.0, 1.0], AMBER_D, "Baseline", False),
        ([2.0, 2.5, 1.5, 1.0, 2.0, 1.5, 2.5, 1.0], LEARN, "Q1 2026", False),
        ([2.5, 3.0, 2.0, 1.5, 2.5, 2.0, 3.0, 1.5], GREEN, "Q3 2026", True),
    ], label_size=12.5)
    with s.g("score table"):
        ty = y0 + 600
        s.line(X0 + 24, ty, X0 + lw - 24, ty, LINE)
        cw = (lw - 48) / 8
        now = [2.5, 3.0, 2.0, 1.5, 2.5, 2.0, 3.0, 1.5]
        base = [1.5, 2.0, 1.0, 1.0, 1.5, 1.5, 2.0, 1.0]
        for i, (code, _) in enumerate(SIGNALS):
            cx = X0 + 24 + i * cw + cw / 2
            on = code == "SS2"
            if on:
                s.rect(cx - cw / 2 + 4, ty + 10, cw - 8, 108, fill=tint(GREEN, 0.08), rx=8, stroke=tint(GREEN, 0.5))
            s.text(cx, ty + 36, code, 13, 700, INK, anchor="middle")
            s.text(cx, ty + 70, f"{now[i]:.1f}", 24, 700, GREEN if on else INK, anchor="middle")
            d = now[i] - base[i]
            s.text(cx, ty + 98, f"+{d:.1f}" if d else "±0", 12.5, 600, STATUS["Approved"] if d else MUTED,
                   anchor="middle")
        s.text(X0 + 24, ty + 142, "Change shown against baseline (Q4 2025). Select a signal to score it.", 12.5, 400, MUTED)

    # ---- scoring panel
    px = X0 + lw + 24
    pw = X1 - px
    with s.g("scoring panel"):
        s.rect(px, y0, pw, ch, fill=CARD, rx=12, stroke=LINE, name="panel bg")
        chip(s, px + 24, y0 + 20, "SS2", LINK, h=24)
        s.text(px + 24, y0 + 74, "Actor collaboration", 22, 700, INK)
        s.text(px + 24, y0 + 98, "Actors across agri-food and energy work together in new ways, beyond the programme.",
               13.5, 400, MUTED)
        y = y0 + 128
        s.text(px + 24, y, "Rubric score", 13, 600, INK2)
        y += 12
        rw = (pw - 48 - 4 * 10) / 5
        for i, (n, lab, desc) in enumerate(RUBRIC):
            cx = px + 24 + i * (rw + 10)
            on = n == 3
            with s.g(f"rubric {n}"):
                s.rect(cx, y, rw, 172, fill=tint(GREEN, 0.08) if on else CARD, rx=10, stroke=GREEN if on else LINE,
                       sw=2 if on else 1)
                s.text(cx + 16, y + 38, str(n), 28, 700, GREEN if on else INK)
                radio(s, cx + rw - 24, y + 26, on)
                s.text(cx + 16, y + 64, lab, 13.5, 600, INK)
                para(s, cx + 16, y + 86, desc, rw - 26, 12, 400, INK2, lh=17, max_lines=5)
        y += 190
        s.text(px + 24, y, "Justification", 13, 600, INK2)
        s.text(px + pw - 24, y, "required", 12, 400, MUTED, anchor="end")
        y += 10
        s.rect(px + 24, y, pw - 48, 104, fill=CARD, rx=8, stroke=GREEN, sw=1.5, name="justification box")
        para(s, px + 40, y + 26, "Collaboration is now repeated and self-funded in 3 regions: Lira farmer groups and "
                                 "NARO run a joint learning platform; Masaka SACCOs co-design solar dryer loans with "
                                 "USEA members; district production offices co-host demos. Western region still "
                                 "programme-led.", pw - 80, 13.5, 400, INK, lh=21)
        y += 124
        s.text(px + 24, y, "Linked approved outcomes (4)", 13, 600, INK2)
        s.text(px + pw - 24, y, "+ Link outcome", 13, 600, GREEN, anchor="end")
        y += 12
        for code, t in [("OH-047", "Lira farmer groups formed a joint RA-PURE learning platform with NARO"),
                        ("OH-044", "Masaka SACCOs co-designed solar dryer asset loans with USEA members"),
                        ("OH-039", "Jinja youth groups set up a solar cold-room enterprise"),
                        ("OH-031", "Kayunga extension workers test soil health on routine visits")]:
            s.rect(px + 24, y, pw - 48, 38, fill="#F7F9F6", rx=8)
            s.icon("sprout", px + 36, y + 10, 18, GREEN, 1.8)
            s.text(px + 62, y + 24, code, 12.5, 700, INK2)
            s.text(px + 126, y + 24, t, 13, 400, INK, maxw=pw - 190)
            s.icon("eye", px + pw - 56, y + 10, 18, MUTED)
            s.link(px + 24, y, pw - 48, 38, "w07")
            y += 44
        y += 8
        fw = (pw - 48 - 16) / 2
        field(s, px + 24, y, fw, "Reviewer notes (internal)", "Revisit Western region in Q4", h=40, size=13)
        field(s, px + 40 + fw, y, fw, "Scored by / date", "Grace Akello · 16 Sep 2026", h=40, size=13, icon="calendar")
        y = y0 + ch - 70
        s.line(px, y - 14, px + pw, y - 14, LINE)
        s.text(px + 24, y + 26, "Previous score 2.5 (Q1 2026) → 3.0", 13, 600, INK2)
        button(s, px + pw - 24, y, "Save score", "primary", icon="check", anchor="end", h=44)
        button(s, px + pw - 170, y, "Save draft", "secondary", anchor="end", h=44)
    return s


# =====================================================================================
def w09_gis():
    s = shell("09 GIS & maps", "GIS & maps", ["Programme", "GIS & maps"])
    mx0, my0 = X0, Y0
    mw, mh = CW - 400, H - 28 - Y0
    with s.g("map frame"):
        s.rect(mx0, my0, mw, mh, fill="#E5EDF1", rx=12, stroke=LINE, name="map water bg")
    m = UgandaMap(mx0 + 60, my0 + 20, mw - 120, mh - 40)
    m.draw_base(s, fill="#F1F3EE", stroke="#DCE2DB", sw=0.8)
    m.draw_programme(s, "region", sw=1.4)
    with s.g("water labels"):
        s.text(mx0 + mw * 0.55, my0 + mh * 0.86, "Lake Victoria", 14, 400, "#6F93A6", name="lake victoria")
    # NREP operational area outline
    with s.g("partner area NREP"):
        for n in PARTNER_AREAS["NREP"]:
            s.path(m.d(n), fill="none", stroke=INK, sw=2.4, dash="7 5", name=n)
    # activity locations
    with s.g("activity locations (GPS)"):
        for n in P4FP_DISTRICTS:
            for (px, py) in m.random_points(n, 5, 3):
                s.circle(px, py, 3.2, fill="#FFFFFF", stroke=INK, sw=1.4)
    # adoption bubbles
    with s.g("adoption hotspots"):
        for n, v in ADOPTION.items():
            cx, cy = m.centroid(n)
            s.circle(cx, cy, 6 + 20 * math.sqrt(v / 2480), fill=AMBER, op=0.55, stroke=AMBER_D, sw=1.5, name=n)
    m.labels(s, 12)
    # popup on Lira
    cx, cy = m.centroid("Lira")
    with s.g("district popup Lira"):
        bx, by = cx + 70, cy - 190
        s.path(f"M{cx + 8:.1f} {cy - 4:.1f} L{bx:.1f} {by + 150:.1f} L{bx:.1f} {by + 180:.1f} Z", fill=CARD,
               stroke=LINE)
        s.rect(bx, by, 300, 214, fill=CARD, rx=12, stroke=LINE)
        s.rect(bx - 1, by + 151, 3, 28, fill=CARD)
        s.text(bx + 20, by + 32, "Lira", 17, 700, INK)
        chip(s, bx + 64, by + 15, "Lango", REGION["Lango"], h=22, size=11)
        rows = [("Farmers adopting (SS5)", "1,580"), ("Solar units installed", "136"), ("Activities (GPS)", "29"),
                ("Approved outcomes", "6"), ("Partners", "NREP · USEA · ACSA · ACME")]
        y = by + 62
        for k, v in rows:
            s.text(bx + 20, y, k, 12.5, 400, MUTED)
            s.text(bx + 280, y, v, 12.5, 600, INK, anchor="end")
            y += 26
        s.text(bx + 20, by + 196, "Open district profile →", 13, 600, GREEN)
    # map tools
    with s.g("map tools"):
        tx, ty = mx0 + 20, my0 + 20
        for ic in ("plus", "minus", None, "crosshair", "layers", "download"):
            if ic is None:
                ty += 10
                continue
            s.rect(tx, ty, 40, 40, fill=CARD, rx=8, stroke=LINE, name=f"tool {ic}")
            if ic == "minus":
                s.path(f"M{tx + 13} {ty + 20} H{tx + 27}", stroke=INK2, sw=2)
            else:
                s.icon(ic, tx + 10, ty + 10, 20, INK2)
            ty += 46
    with s.g("legend"):
        lx, ly = mx0 + 76, my0 + 20
        s.rect(lx, ly, 280, 176, fill=CARD, rx=10, stroke=LINE)
        s.text(lx + 16, ly + 28, "Programme regions", 12.5, 600, INK)
        for i, (r, c) in enumerate(REGION.items()):
            xx = lx + 16 + (i % 2) * 130
            yy = ly + 44 + (i // 2) * 24
            s.rect(xx, yy, 14, 14, fill=c, op=0.8, rx=3)
            s.text(xx + 22, yy + 12, r, 12.5, 400, INK2)
        s.circle(lx + 23, ly + 112, 9, fill=AMBER, op=0.55, stroke=AMBER_D, sw=1.5)
        s.text(lx + 40, ly + 116, "Farmers adopting RA-PURE", 12.5, 400, INK2)
        s.circle(lx + 23, ly + 136, 4, fill="#FFFFFF", stroke=INK, sw=1.4)
        s.text(lx + 40, ly + 140, "Activity location (GPS)", 12.5, 400, INK2)
        s.line(lx + 14, ly + 160, lx + 32, ly + 160, INK, 2.2, dash="5 3")
        s.text(lx + 40, ly + 164, "Selected partner area (NREP)", 12.5, 400, INK2)
    s.text(mx0 + mw - 16, my0 + mh - 14, "Boundaries: UBOS · Leaflet + OpenStreetMap in the live system", 11, 400,
           MUTED, anchor="end")

    # ---- layer panel
    px = mx0 + mw + 20
    pw = X1 - px
    with s.g("layer panel"):
        s.rect(px, Y0, pw, mh, fill=CARD, rx=12, stroke=LINE, name="panel bg")
        s.text(px + 24, Y0 + 38, "Map layers", 17, 600, INK)
        s.text(px + 24, Y0 + 60, "Only approved records are drawn", 13, 400, MUTED)
        y = Y0 + 92
        layers = [("Programme districts (15)", True, "by region"), ("Partner operational areas", True, "NREP selected"),
                  ("RA-PURE adoption hotspots", True, "SS5 · PHI 8"), ("Activity locations (GPS)", True, "412 points"),
                  ("Approved outcomes", False, "64 · where geographic"), ("Coverage gaps & overlaps", False, "analysis"),
                  ("Sub-county boundaries", False, "admin layer")]
        for t, on, sub in layers:
            toggle(s, px + 24, y, on)
            s.text(px + 72, y + 9, t, 13.5, 600 if on else 400, INK if on else INK2)
            s.text(px + 72, y + 27, sub, 12, 400, MUTED)
            y += 48
        s.line(px + 24, y, px + pw - 24, y, LINE)
        y += 26
        s.text(px + 24, y, "Partner", 13, 600, INK2)
        y += 12
        for i, p in enumerate(PARTNERS):
            cx = px + 24 + (i % 2) * ((pw - 48) / 2)
            cy = y + (i // 2) * 30
            checkbox(s, cx, cy + 2, p == "NREP")
            s.text(cx + 28, cy + 16, p, 13, 400, INK)
        y += 4 * 30 + 16
        field(s, px + 24, y, pw - 48, "Value chain", "All value chains", h=40, dropdown=True, size=13)
        y += 78
        field(s, px + 24, y, pw - 48, "Colour districts by", "Programme region", h=40, dropdown=True, size=13)
        y = Y0 + mh - 118
        s.rect(px + 24, y, pw - 48, 94, fill=tint(GREEN, 0.07), rx=10)
        s.icon("plus", px + 38, y + 16, 18, GREEN, 2.2)
        s.text(px + 64, y + 30, "Add a district or GIS layer", 13.5, 600, GREEN_D)
        para(s, px + 40, y + 54, "Administrators can upload new boundaries (GeoJSON / shapefile) as the programme "
                                 "expands beyond 15 districts.", pw - 80, 12, 400, INK2, lh=17)
    return s


# =====================================================================================
def w10_partner_home():
    s = shell("10 Partner portal home (NREP)", "My dashboard", ["NREP", "My dashboard"], user=PARTNER_USER,
              nav=NAV_PARTNER)
    s.text(X0, Y0 + 30, "Good morning, Brian", 26, 700, INK)
    s.text(X0, Y0 + 56, "NREP workspace · you see NREP data only. Programme-wide figures are shared by SNV.", 14, 400,
           MUTED)
    button(s, X1, Y0 + 12, "Harvest an outcome", "secondary", icon="plus", anchor="end")

    # due banner
    by = Y0 + 84
    with s.g("due banner"):
        s.rect(X0, by, CW, 96, fill=GREEN_D, rx=12)
        s.circle(X0 + 56, by + 48, 26, fill="#FFFFFF", op=0.12)
        s.icon("calendar", X0 + 44, by + 36, 24, "#FFFFFF", 2)
        s.text(X0 + 100, by + 40, "Q3 2026 quarterly report is due in 6 days (30 Sep)", 18, 700, "#FFFFFF")
        s.text(X0 + 100, by + 66, "Technical report 80% complete · financial report not started · 2 evidence files "
                                  "still needed", 14, 400, "#CFE3D7")
        for i, (lab, fr) in enumerate([("Technical", 0.8), ("Financial", 0.0)]):
            xx = X0 + 1030 + i * 190
            s.text(xx, by + 38, lab, 12.5, 600, "#CFE3D7")
            progress(s, xx, by + 50, 160, fr, AMBER, h=8, bg="#2F6B4E")
            s.text(xx, by + 78, f"{round(fr * 100)}%", 13, 700, "#FFFFFF")
        button(s, X1 - 24, by + 28, "Continue report", "primary", icon="arrowright", anchor="end", color=AMBER)

    s.link(X0, by, CW, 96, "w11")
    # returned alert
    ay = by + 112
    s.link(X0, ay, CW, 60, "w10c")
    with s.g("returned alert"):
        s.rect(X0, ay, CW, 60, fill=tint(STATUS["Returned"], 0.08), rx=10, stroke=tint(STATUS["Returned"], 0.4))
        s.icon("arrowleft", X0 + 20, ay + 20, 20, STATUS["Returned"], 2.2)
        s.text(X0 + 52, ay + 26, "SNV returned 1 outcome for revision:", 14, 600, INK)
        s.text(X0 + 52 + tw("SNV returned 1 outcome for revision:", 14, 600) + 6, ay + 26,
               "“Isingiro dairy cooperative adopted solar milk chilling…”", 14, 400, INK2)
        s.text(X0 + 52, ay + 45, "Grace Akello: add the cooperative's before/after spoilage records as evidence.",
               12.5, 400, MUTED)
        button(s, X1 - 20, ay + 12, "Fix and resubmit", "danger", anchor="end", h=36)

    ky = ay + 80
    kw = (CW - 3 * 20) / 4
    for i, (ic, col, lab, val, sub, fr) in enumerate([
            ("target", GREEN, "My indicators on track", "7 of 9", "2 behind: OI 4.1, OI 4.2", 7 / 9),
            ("sprout", LINK, "My outcomes approved", "12", "2 under review · 1 returned", None),
            ("listcheck", LEARN, "Workplan activities", "18 of 26", "complete · 3 due this month", 18 / 26),
            ("coins", AMBER, "Sub-grant tranche 3", "UGX 184M", "of 280M disbursed · 66%", 0.66)]):
        kpi(s, X0 + i * (kw + 20), ky, kw, 150, ic, col, lab, val, sub, fr)

    ry = ky + 170
    rh = H - 28 - ry
    c1 = 640
    card(s, X0, ry, c1, rh, "My indicator progress", "NREP's contribution · approved values", action="All 9 →")
    y = ry + 104
    step = (rh - 116) / 5
    for name, code, v, t_, fr, col, note in [
            ("Farmers adopting RA-PURE", "PHI 8", "3,940", "9,000", 0.44, GREEN, "+1,020 this quarter · under SNV review"),
            ("Solar irrigation units installed", "OI 2.3", "388", "800", 0.49, GREEN, "+74 this quarter · GPS on all"),
            ("Agribusinesses using PURE", "OI 2.1", "64", "120", 0.53, GREEN, "+18 this quarter"),
            ("Policy engagements with evidence", "OI 4.1", "3", "12", 0.25, AMBER, "Behind plan · 2 planned in Q4"),
            ("Finance mobilised (EUR)", "OI 4.2", "€0.21M", "€1.0M", 0.21, AMBER, "Mbarara budget line pending approval")]:
        s.text(X0 + 24, y, name, 14, 600, INK, maxw=300)
        s.text(X0 + 24, y + 20, note, 12.5, 400, MUTED, maxw=330)
        s.text(X0 + 356, y, code, 12, 600, MUTED)
        progress(s, X0 + 356, y + 12, 140, fr, col, h=8)
        s.text(X0 + c1 - 24, y, f"{v}", 14, 700, INK, anchor="end")
        s.text(X0 + c1 - 24, y + 20, f"of {t_}", 12.5, 400, MUTED, anchor="end")
        s.line(X0 + 24, y + step - 32, X0 + c1 - 24, y + step - 32, LINE2)
        y += step

    c2x = X0 + c1 + 20
    c2 = 560
    card(s, c2x, ry, c2, rh, "Workplan · Q3–Q4 2026", "Planned vs actual", action="Open →")
    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    gx = c2x + 210
    gw = c2 - 210 - 24
    for i, mth in enumerate(months):
        s.text(gx + gw * (i + 0.5) / 6, ry + 92, mth, 11.5, 600, MUTED, anchor="middle")
    s.line(gx + gw * 2.8 / 6, ry + 100, gx + gw * 2.8 / 6, ry + rh - 20, STATUS["Overdue"], 1.5, dash="3 3")
    acts = [("Farmer field schools · Isingiro", 0, 3, "Complete"), ("Solar pump demos · Mbarara", 1, 3.5, "On track"),
            ("District budget dialogues", 1.5, 2.6, "Complete"), ("Cold-chain feasibility study", 2, 5, "At risk"),
            ("Dealer finance workshop · Lira", 3, 4, "On track"), ("Q4 learning exchange", 4.5, 6, "On track")]
    y = ry + 112
    step = (rh - 130) / len(acts)
    for name, a, b, st in acts:
        s.text(c2x + 24, y + 14, name, 12.5, 400, INK, maxw=180)
        col = STATUS[st]
        s.rect(gx + gw * a / 6, y + 2, gw * (b - a) / 6, 18, fill=tint(col, 0.3), rx=5)
        done = min(max((2.8 - a) / (b - a), 0), 1) if st != "Complete" else 1
        s.rect(gx + gw * a / 6, y + 2, gw * (b - a) / 6 * done, 18, fill=col, rx=5)
        y += step

    c3x = c2x + c2 + 20
    c3 = X1 - c3x
    card(s, c3x, ry, c3, rh, "Where NREP works", "Mbarara · Isingiro · Ntungamo · Lira")
    s.link(c3x, ry, c3, rh, "w09p")
    m = UgandaMap(c3x + 16, ry + 76, c3 - 32, rh - 250)
    m.draw_base(s, fill="#EEF1EC")
    with s.g("programme districts"):
        for n in P4FP_DISTRICTS:
            on = n in PARTNER_AREAS["NREP"]
            s.path(m.d(n), fill=GREEN if on else tint(GREEN, 0.25), op=0.9 if on else None, stroke="#FFFFFF", sw=0.8,
                   name=n)
    y = ry + rh - 160
    s.line(c3x + 24, y - 8, c3x + c3 - 24, y - 8, LINE2)
    for n, v in [("Mbarara", "1,420"), ("Isingiro", "1,160"), ("Lira", "890"), ("Ntungamo", "470")]:
        s.rect(c3x + 24, y + 4, 12, 12, fill=GREEN, rx=3)
        s.text(c3x + 44, y + 15, n, 13.5, 400, INK)
        s.text(c3x + c3 - 24, y + 15, v + " farmers", 13, 600, INK2, anchor="end")
        y += 34
    return s


# =====================================================================================
def w11_report_form():
    s = shell("11 Partner quarterly report form", "Quarterly reports", ["NREP", "Quarterly reports", "Q3 2026 technical"],
              user=PARTNER_USER, nav=NAV_PARTNER)
    with s.g("form header"):
        s.text(X0, Y0 + 30, "Q3 2026 technical report", 26, 700, INK)
        x = X0
        x += status_chip(s, x, Y0 + 44, "Draft") + 10
        s.icon("check", x, Y0 + 48, 16, STATUS["Approved"], 2.4)
        s.text(x + 22, Y0 + 61, "Saved 2 minutes ago · works offline", 13, 400, MUTED)
        bx = X1
        nb = button(s, bx, Y0 + 12, "Next: Activities", "primary", icon="arrowright", anchor="end")
        s.link(bx - nb, Y0 + 12, nb, 40, "w10")
        bx -= nb + 12
        button(s, bx, Y0 + 12, "Save draft", "secondary", anchor="end")

    # stepper
    sy = Y0 + 92
    steps = ["Period & summary", "Indicator results", "Activities & workplan", "Financial summary", "Outcomes",
             "Evidence", "Review & submit"]
    with s.g("stepper"):
        s.rect(X0, sy, CW, 64, fill=CARD, rx=12, stroke=LINE)
        sw_ = CW / len(steps)
        for i, t in enumerate(steps):
            cx = X0 + i * sw_ + 24
            done, on = i < 1, i == 1
            col = GREEN if (done or on) else FAINT
            s.circle(cx + 14, sy + 32, 14, fill=col if (done or on) else CARD, stroke=col, sw=1.5)
            if done:
                s.icon("check", cx + 6, sy + 24, 16, "#FFFFFF", 2.6)
            else:
                s.text(cx + 14, sy + 37, str(i + 1), 13, 700, "#FFFFFF" if on else MUTED, anchor="middle")
            s.text(cx + 38, sy + 37, t, 13.5, 600 if on else 400, INK if (on or done) else MUTED)
            if i < len(steps) - 1:
                s.line(cx + 44 + tw(t, 13.5, 600), sy + 32, X0 + (i + 1) * sw_ + 14, sy + 32, LINE, 1.5)

    fy = sy + 84
    fw = 1130
    fh = H - 28 - fy
    with s.g("indicator entry"):
        s.rect(X0, fy, fw, fh, fill=CARD, rx=12, stroke=LINE, name="bg")
        x = X0 + 24
        x += chip(s, x, fy + 20, "PHI 8", GREEN) + 8
        x += chip(s, x, fy + 20, "SS5", LINK) + 8
        s.text(X1 - (X1 - X0 - fw) - 24, fy + 38, "Indicator 1 of 6", 13, 400, MUTED, anchor="end")
        s.text(X0 + 24, fy + 78, "Farmers adopting RA-PURE practices this quarter", 20, 700, INK)
        s.text(X0 + 24, fy + 102, "Count each farmer once. Farmers already reported in an earlier quarter are "
                                  "flagged automatically.", 13.5, 400, MUTED)
        # disaggregation grid
        gy = fy + 130
        s.text(X0 + 24, gy + 14, "Disaggregation", 13, 600, INK2)
        s.text(X0 + 24 + tw("Disaggregation", 13, 600) + 8, gy + 14, "*", 13, 600, STATUS["Rejected"])
        gy += 28
        colx = [X0 + 24, X0 + 244, X0 + 424, X0 + 604]
        s.rect(X0 + 24, gy, 760, 40, fill="#F7F9F6", rx=8)
        for cx, t in zip(colx, ["", "Youth 18–35", "Adults 36+", "Total"]):
            s.text(cx + 16, gy + 25, t, 12, 600, MUTED)
        vals = [("Women", "214", "338", "552"), ("Men", "170", "298", "468")]
        yy = gy + 48
        for lab, a, b, t in vals:
            s.text(colx[0] + 16, yy + 27, lab, 14, 600, INK)
            for cx, v in zip(colx[1:3], (a, b)):
                s.rect(cx, yy + 4, 160, 40, fill=CARD, rx=8, stroke="#CFD6D1")
                s.text(cx + 14, yy + 29, v, 14, 400, INK)
            s.text(colx[3] + 16, yy + 29, t, 15, 700, INK)
            yy += 52
        s.line(X0 + 24, yy + 4, X0 + 784, yy + 4, LINE)
        s.text(colx[0] + 16, yy + 32, "Total", 14, 700, INK)
        s.text(colx[1] + 16, yy + 32, "384", 14, 600, INK2)
        s.text(colx[2] + 16, yy + 32, "636", 14, 600, INK2)
        s.text(colx[3] + 16, yy + 32, "1,020", 18, 700, GREEN_D)
        s.text(colx[3] + 16, yy + 52, "auto-calculated", 11.5, 400, MUTED)
        # side fields
        sx = X0 + 820
        field(s, sx, fy + 150, fw - 820 - 24, "Districts", "Mbarara, Isingiro, Lira", h=44, dropdown=True, required=True,
              icon="pin")
        field(s, sx, fy + 232, fw - 820 - 24, "Value chains", "Dairy, Horticulture", h=44, dropdown=True, required=True)
        # warnings
        wy = yy + 80
        with s.g("validation messages"):
            s.rect(X0 + 24, wy, fw - 48, 86, fill=tint(STATUS["Under review"], 0.08), rx=10,
                   stroke=tint(STATUS["Under review"], 0.4))
            s.icon("alert", X0 + 42, wy + 18, 20, AMBER_D, 2)
            s.text(X0 + 74, wy + 33, "1,020 is 65% higher than last quarter (620)", 14, 600, INK)
            s.text(X0 + 74, wy + 55, "That can be right — add a short explanation so SNV can approve it faster.", 13,
                   400, INK2)
            s.text(X0 + 74, wy + 74, "Explanation added ✓", 12.5, 600, STATUS["Approved"])
            wy += 100
            s.rect(X0 + 24, wy, fw - 48, 86, fill=tint(STATUS["Returned"], 0.07), rx=10,
                   stroke=tint(STATUS["Returned"], 0.4))
            s.icon("users", X0 + 42, wy + 18, 20, STATUS["Returned"], 2)
            s.text(X0 + 74, wy + 33, "Possible duplicates: 12 farmers match people NOGAMU reported in Q2", 14, 600, INK)
            s.text(X0 + 74, wy + 55, "Matched on phone number, name and village. Review them before submitting — "
                                     "duplicates are not counted twice.", 13, 400, INK2)
            button(s, X0 + fw - 44, wy + 24, "Review 12 matches", "danger", anchor="end", h=36, size=13)
        # evidence
        ey = wy + 108
        s.text(X0 + 24, ey + 14, "Evidence", 13, 600, INK2)
        s.text(X0 + 24 + tw("Evidence", 13, 600) + 8, ey + 14, "required: adoption register", 12.5, 400, MUTED)
        ey += 26
        s.rect(X0 + 24, ey, 520, 64, fill="#F7F9F6", rx=10, stroke=LINE)
        s.rect(X0 + 38, ey + 12, 40, 40, fill=tint(GREEN, 0.12), rx=8)
        s.icon("file", X0 + 47, ey + 21, 22, GREEN)
        s.text(X0 + 92, ey + 29, "Adoption register – Isingiro & Mbarara – Sep 2026.xlsx", 13.5, 600, INK, maxw=400)
        s.text(X0 + 92, ey + 48, "1,020 rows · GPS on 1,020 · 348 KB", 12, 400, MUTED)
        s.rect(X0 + 560, ey, fw - 584, 64, fill=CARD, rx=10, stroke="#B9C3BC", dash="6 4")
        s.icon("upload", X0 + 580, ey + 21, 22, GREEN)
        s.text(X0 + 614, ey + 30, "Drop files or take photos", 13.5, 600, GREEN_D)
        s.text(X0 + 614, ey + 49, "PDF, Excel, JPG, PNG · up to 25 MB", 12, 400, MUTED)

    # ---- checklist panel
    px = X0 + fw + 20
    pw = X1 - px
    with s.g("report checklist"):
        s.rect(px, fy, pw, fh, fill=CARD, rx=12, stroke=LINE, name="bg")
        s.text(px + 24, fy + 38, "Indicators in this report", 16, 600, INK)
        y = fy + 64
        for code, name, st in [("PHI 8", "Farmers adopting RA-PURE", "active"), ("OI 2.1", "Agribusinesses using PURE", "done"),
                               ("OI 2.3", "Solar units installed", "done"), ("OI 3.1", "People trained", "done"),
                               ("OI 3.4", "Multi-actor platforms", "missing"), ("OI 4.1", "Policy engagements", "todo")]:
            on = st == "active"
            if on:
                s.rect(px + 12, y - 4, pw - 24, 52, fill=tint(GREEN, 0.08), rx=8)
            ic, col = {"done": ("check", STATUS["Approved"]), "active": ("edit", GREEN),
                       "missing": ("alert", STATUS["Returned"]), "todo": ("clock", FAINT)}[st]
            s.icon(ic, px + 26, y + 10, 18, col, 2.2)
            s.text(px + 56, y + 18, code, 12, 700, INK2)
            s.text(px + 56, y + 36, name, 13, 400 if not on else 600, INK)
            y += 56
        y += 10
        s.line(px + 24, y, px + pw - 24, y, LINE)
        y += 30
        s.text(px + 24, y, "Before you submit", 14, 600, INK)
        y += 10
        for ok, t in [(True, "All mandatory fields"), (True, "Explanations for unusual values"),
                      (False, "Evidence for every result (5 of 6)"), (False, "Duplicates reviewed")]:
            y += 30
            s.icon("check" if ok else "x", px + 24, y - 14, 18, STATUS["Approved"] if ok else STATUS["Returned"], 2.4)
            s.text(px + 52, y, t, 13, 400, INK if ok else INK2)
        y += 34
        s.rect(px + 24, y, pw - 48, 110, fill=tint(AMBER, 0.12), rx=10)
        s.icon("wifioff", px + 40, y + 16, 20, AMBER_D, 2)
        s.text(px + 70, y + 31, "Poor connection?", 13.5, 600, INK)
        para(s, px + 40, y + 58, "Keep typing. The report saves on this device and uploads itself when you are back "
                                 "online.", pw - 80, 12.5, 400, INK2, lh=19)
    return s


# =====================================================================================
def w12_library():
    s = shell("12 Knowledge library", "Knowledge library", ["Knowledge", "Knowledge library"])
    page_head(s, "Knowledge library", "Studies, learning briefs, success stories, business cases and media from SNV "
                                      "and partners — tagged, searchable and linked to the evidence behind them")
    x = X1
    x -= button(s, x, Y0 + 12, "Submit a product", "primary", icon="upload", anchor="end") + 12
    x -= button(s, x, Y0 + 12, "Learning brief template", "secondary", icon="file", anchor="end") + 12
    button(s, x, Y0 + 12, "Success story template", "secondary", icon="file", anchor="end")

    fy = Y0 + 84
    fw = 300
    with s.g("filters"):
        s.rect(X0, fy, fw, H - 28 - fy, fill=CARD, rx=12, stroke=LINE)
        s.text(X0 + 20, fy + 34, "Filters", 16, 600, INK)
        s.text(X0 + fw - 20, fy + 34, "Clear", 13, 600, GREEN, anchor="end")
        y = fy + 60
        for grp, opts in [("Type", [("Learning brief", 14, True), ("Success story", 22, True), ("Business case", 9, False),
                                    ("Research / study", 7, False), ("Policy brief", 5, False), ("Media product", 31, False)]),
                          ("Pathway", [("LEARN", 38, False), ("LINK", 29, False), ("LEVERAGE", 21, False)]),
                          ("System Signal", [("SS1 – SS4", 34, False), ("SS5 – SS8", 41, False)]),
                          ("Status", [("Published", 58, False), ("Under review", 6, False), ("Internal only", 12, False)])]:
            s.text(X0 + 20, y + 12, grp, 12.5, 600, MUTED)
            y += 22
            for lab, n, on in opts:
                checkbox(s, X0 + 20, y + 3, on, 16)
                s.text(X0 + 46, y + 16, lab, 13, 400, INK)
                s.text(X0 + fw - 20, y + 16, str(n), 12, 400, MUTED, anchor="end")
                y += 28
            y += 12
        field(s, X0 + 20, y, fw - 40, "Partner", "All partners", h=38, dropdown=True, size=13)
        y += 74
        field(s, X0 + 20, y, fw - 40, "District", "All districts", h=38, dropdown=True, size=13)

    gx = X0 + fw + 24
    gw = X1 - gx
    with s.g("search"):
        s.rect(gx, fy, gw, 46, fill=CARD, rx=10, stroke=LINE)
        s.icon("search", gx + 16, fy + 13, 20, MUTED)
        s.text(gx + 48, fy + 29, "solar dryer coffee", 14, 400, INK)
        s.text(gx + gw - 16, fy + 29, "36 results · sorted by newest", 13, 400, MUTED, anchor="end")
    items = [
        ("Success story", GREEN, "sun", "From drying on tarpaulins to solar dryers: Masaka's coffee women", "USEA", ["SS5", "SS8", "LINK"], "Published", "Sep 2026", "Coffee · Masaka"),
        ("Learning brief", LEARN, "book", "What makes farmers keep a regenerative practice after year one?", "NOGAMU", ["SS1", "LEARN"], "Published", "Aug 2026", "All value chains"),
        ("Business case", AMBER_D, "coins", "Pay-as-you-go solar pumps for farmer groups: the numbers", "CREEC", ["SS4", "SS6", "LINK"], "Under review", "Sep 2026", "Horticulture · Mbale"),
        ("Policy brief", LEVERAGE, "flag", "Budgeting for PURE: a note for district production offices", "NREP", ["SS3", "LEVERAGE"], "Published", "Jul 2026", "Western region"),
        ("Media product", LINK, "mic", "Radio series: 'Healthy Soils, Better Harvests' — 12 episodes", "ACME", ["SS1", "LEARN"], "Published", "Jun 2026", "Kasese · Mbarara"),
        ("Research / study", "#0F766E", "bars", "Baseline: energy use in dairy cold chains, 15 districts", "NARO", ["SS5", "LEARN"], "Internal only", "Mar 2026", "Dairy"),
    ]
    cw = (gw - 2 * 20) / 3
    chh = (H - 28 - fy - 66 - 20) / 2
    for i, (typ, col, ic, title, partner, tags, st, date, meta) in enumerate(items):
        x = gx + (i % 3) * (cw + 20)
        y = fy + 66 + (i // 3) * (chh + 20)
        with s.g(f"product {title[:24]}"):
            s.rect(x, y, cw, chh, fill=CARD, rx=12, stroke=LINE)
            s.rect(x, y, cw, 150, fill=tint(col, 0.12), rx=12, name="thumb")
            s.rect(x, y + 138, cw, 12, fill=tint(col, 0.12), name="thumb bottom")
            s.circle(x + cw - 70, y + 70, 56, fill=tint(col, 0.2))
            s.icon(ic, x + cw - 94, y + 46, 48, col, 1.6)
            chip(s, x + 20, y + 20, typ, col, solid=True, h=26)
            if st == "Internal only":
                chip(s, x + 20, y + 108, "Internal only — not public", STATUS["Rejected"], icon="lock", h=26)
            ty = y + 186
            for ln in wrap(title, cw - 40, 16, 600)[:2]:
                s.text(x + 20, ty, ln, 16, 600, INK)
                ty += 24
            s.text(x + 20, ty + 6, f"{partner} · {date} · {meta}", 12.5, 400, MUTED, maxw=cw - 40)
            tx = x + 20
            for t in tags:
                tx += chip(s, tx, ty + 22, t, PATHWAY.get(t, "#5B6770"), h=22, size=11) + 6
            s.line(x + 20, y + chh - 50, x + cw - 20, y + chh - 50, LINE2)
            status_chip(s, x + 20, y + chh - 37, st if st != "Internal only" else "Approved", h=24)
            s.icon("link", x + cw - 120, y + chh - 32, 16, MUTED, 2)
            s.text(x + cw - 98, y + chh - 19, f"{[3, 2, 4, 5, 1, 2][i]} linked", 12.5, 400, MUTED)
    return s


# =====================================================================================
def w13_logalto():
    s = shell("13 LogAlto exchange & exports", "LogAlto & exports", ["Administration", "LogAlto & exports"])
    page_head(s, "LogAlto exchange & exports", "The MEL platform complements LogAlto: approved P4FP results flow to "
                                               "SNV's corporate system, and every record can leave as CSV, Excel or PDF")
    button(s, X1, Y0 + 12, "Run sync now", "primary", icon="refresh", anchor="end")

    y0 = Y0 + 84
    # flow diagram card
    card(s, X0, y0, CW, 200, None)
    with s.g("data flow"):
        boxes = [("Partners & field app", "Reports, adoption records, outcomes, evidence", "users", LEARN),
                 ("SNV MEL review", "Validate · return · approve", "shield", AMBER_D),
                 ("P4FP MEL platform", "Approved data only · audit trail", "database", GREEN),
                 ("LogAlto (SNV corporate)", "Mapped indicators · nightly push", "api", "#5B6770")]
        bw = 330
        gap = (CW - 48 - 4 * bw) / 3
        for i, (t, sub, ic, col) in enumerate(boxes):
            x = X0 + 24 + i * (bw + gap)
            s.rect(x, y0 + 40, bw, 120, fill=tint(col, 0.08), rx=12, stroke=tint(col, 0.4))
            s.rect(x + 20, y0 + 60, 44, 44, fill=col, rx=10)
            s.icon(ic, x + 30, y0 + 70, 24, "#FFFFFF", 2)
            s.text(x + 80, y0 + 80, t, 15, 700, INK)
            para(s, x + 80, y0 + 102, sub, bw - 100, 12.5, 400, INK2, lh=18)
            if i < 3:
                ax = x + bw + 10
                s.line(ax, y0 + 100, ax + gap - 20, y0 + 100, INK2, 2)
                s.path(f"M{ax + gap - 28} {y0 + 94} L{ax + gap - 20} {y0 + 100} L{ax + gap - 28} {y0 + 106}", stroke=INK2,
                       sw=2)
        s.text(X0 + 24 + 3 * (bw + gap) - gap / 2, y0 + 88, "API", 12, 700, INK2, anchor="middle")
        s.text(X0 + 24 + 3 * (bw + gap) - gap / 2, y0 + 128, "or Excel pack", 11.5, 400, MUTED, anchor="middle")

    ry = y0 + 220
    rh = H - 28 - ry
    lw = 1000
    card(s, X0, ry, lw, rh, "Indicator mapping to LogAlto", "Set up with SNV's LogAlto focal point at inception",
         action="Edit mapping")
    cols = [("P4FP indicator", 330, "start"), ("LogAlto indicator", 220, "start"), ("Last value pushed", 150, "end"),
            ("Sync", lw - 700 - 2, "start")]

    def sc(v, note=""):
        def f(s_, x, y, w, h):
            col = {"Synced": STATUS["Approved"], "Queued": STATUS["Under review"], "Conflict": STATUS["Returned"],
                   "Not mapped": MUTED}[v]
            chip(s_, x + 16, y + h / 2 - 12, v, col, dot=True)
            if note:
                s_.text(x + 28 + tw(v, 12, 600) + 30, y + h / 2 + 4.5, note, 12, 400, MUTED)
        return f

    rows = [["PHI 8 · Farmers adopting RA-PURE", "SNV-AGR-03", "18,420", sc("Synced", "24 Sep 02:00")],
            ["OI 1.2 · Hectares under RA", "SNV-AGR-07", "8,960 ha", sc("Synced", "24 Sep 02:00")],
            ["OI 2.1 · Agribusinesses using PURE", "SNV-ENE-11", "312", sc("Synced", "24 Sep 02:00")],
            ["OI 2.3 · Solar units installed", "SNV-ENE-04", "1,146", sc("Queued", "74 new approved")],
            ["OI 3.1 · People trained", "SNV-CAP-01", "24,870", sc("Conflict", "LogAlto shows 24,210")],
            ["OI 4.2 · Finance mobilised", "SNV-FIN-02", "€1.9M", sc("Synced", "24 Sep 02:00")],
            ["SS1–SS8 · Signal scores", "—", "—", sc("Not mapped", "P4FP-only · export only")]]
    table(s, X0 + 1, ry + 80, cols, rows, row_h=(rh - 80 - 40 - 16) / 7, head_h=40)

    px = X0 + lw + 20
    pw = X1 - px
    eh = 330
    card(s, px, ry, pw, eh, "Exports", "Validated records only unless you choose otherwise")
    y = ry + 84
    for ic, t, sub, fmts in [("globe", "Donor report extract (IKEA Foundation)", "Indicators + GESI + outcomes, by period", "Excel · PDF"),
                             ("database", "LogAlto import pack", "Fallback when the API is unavailable", "Excel"),
                             ("download", "Full data export", "All records, metadata and attachments", "CSV · Excel · ZIP"),
                             ("sprout", "Outcome harvesting log", "Approved outcomes with evidence links", "Excel · PDF")]:
        s.rect(px + 24, y, pw - 48, 52, fill="#F7F9F6", rx=10)
        s.icon(ic, px + 38, y + 15, 22, GREEN, 1.8)
        s.text(px + 74, y + 23, t, 13.5, 600, INK)
        s.text(px + 74, y + 41, sub, 12, 400, MUTED)
        s.text(px + pw - 40, y + 32, fmts, 12.5, 600, GREEN, anchor="end")
        y += 60
    by = ry + eh + 20
    bh = H - 28 - by
    card(s, px, by, pw, bh, "Daily backups", "Automatic at 02:00 · encrypted · SNV admin can download")
    y = by + 104
    for d, sz in [("24 Sep 2026 · 02:00", "1.24 GB"), ("23 Sep 2026 · 02:00", "1.23 GB"), ("22 Sep 2026 · 02:00", "1.21 GB")]:
        s.icon("check", px + 24, y - 14, 18, STATUS["Approved"], 2.4)
        s.text(px + 52, y, d, 13.5, 400, INK)
        s.text(px + pw - 150, y, sz, 13, 400, MUTED, anchor="end")
        s.text(px + pw - 24, y, "Download", 13, 600, GREEN, anchor="end")
        y += 36
    s.text(px + 24, y - 4, "Restore last tested 02 Sep 2026 · 30 days kept", 12.5, 400, MUTED)
    with s.g("website feed"):
        wy = by + bh - 76
        s.rect(px + 24, wy, pw - 48, 56, fill=tint(LEARN, 0.07), rx=10)
        s.icon("globe", px + 38, wy + 17, 22, LEARN, 1.8)
        s.text(px + 74, wy + 24, "P4FP website feed", 13.5, 600, INK)
        s.text(px + 74, wy + 42, "Approved, non-sensitive summaries only", 12, 400, MUTED)
        toggle(s, px + pw - 76, wy + 18, True, LEARN)
    return s


# =====================================================================================
def w14_users():
    s = shell("14 Users, roles & audit trail", "Users & roles", ["Administration", "Users & roles"])
    page_head(s, "Users, roles & access", "Permissions say what a role can do · scope says whose data it can see")
    x = X1
    x -= button(s, x, Y0 + 12, "Invite user", "primary", icon="plus", anchor="end") + 12
    button(s, x, Y0 + 12, "Security settings", "secondary", icon="shield", anchor="end")

    y0 = Y0 + 84
    lw = 1010
    mh = 470
    card(s, X0, y0, lw, mh, "Role permissions", "Configurable by the Super Administrator")
    roles = ["Super Admin", "SNV MEL Reviewer", "Partner MEL Focal Person", "Partner Field User", "Read-only"]
    perms = [("See programme-wide data", [1, 1, 0, 0, 1]), ("See own partner's data", [1, 1, 1, 1, 0]),
             ("Enter reports & results", [1, 0, 1, 1, 0]), ("Submit to SNV", [1, 0, 1, 0, 0]),
             ("Approve / return submissions", [1, 1, 0, 0, 0]), ("Score System Signals", [1, 1, 0, 0, 0]),
             ("See sub-grant finance", [1, 1, 2, 0, 0]), ("Export data", [1, 1, 2, 0, 3]), ("Manage users", [1, 0, 0, 0, 0])]
    cx0 = X0 + 290
    colw = (lw - 290 - 24) / 5
    with s.g("permission matrix"):
        s.rect(X0 + 1, y0 + 76, lw - 2, 56, fill="#F7F9F6")
        for i, r in enumerate(roles):
            lines = wrap(r, colw - 12, 12.5, 600)
            for j, ln in enumerate(lines):
                s.text(cx0 + i * colw + colw / 2, y0 + 100 + j * 16 - (len(lines) - 1) * 8, ln, 12.5, 600, INK2,
                       anchor="middle")
        y = y0 + 132
        rh = (mh - 132 - 16) / len(perms)
        for p, vals in perms:
            s.line(X0 + 1, y, X0 + lw - 1, y, LINE2)
            s.text(X0 + 24, y + rh / 2 + 4.5, p, 13.5, 400, INK)
            for i, v in enumerate(vals):
                cx = cx0 + i * colw + colw / 2
                if v == 1:
                    s.circle(cx, y + rh / 2, 11, fill=tint(GREEN, 0.14))
                    s.icon("check", cx - 7, y + rh / 2 - 7, 14, GREEN, 2.8)
                elif v in (2, 3):
                    s.text(cx, y + rh / 2 + 4.5, "own only" if v == 2 else "approved only", 11.5, 600, AMBER_D,
                           anchor="middle")
                else:
                    s.rect(cx - 6, y + rh / 2 - 1, 12, 2, fill="#CBD2CD", rx=1)
            y += rh

    uy = y0 + mh + 20
    uh = H - 28 - uy
    card(s, X0, uy, lw, uh, "Users · 46 active", None, action="Manage all →")
    cols = [("Name", 300, "start"), ("Organisation", 170, "start"), ("Role", 230, "start"), ("Last active", 150, "start"),
            ("2-step", lw - 850 - 2, "start")]

    def who(n, e, ini, col):
        def f(s_, x, y, w, h):
            avatar(s_, x + 32, y + h / 2, 15, ini, col)
            s_.text(x + 56, y + h / 2 - 2, n, 13.5, 600, INK)
            s_.text(x + 56, y + h / 2 + 15, e, 12, 400, MUTED)
        return f

    def ok(v):
        return lambda s_, x, y, w, h: chip(s_, x + 16, y + h / 2 - 11, "On" if v else "Pending", STATUS["Approved"] if v else STATUS["Under review"], h=22, size=11, dot=True)

    rows = [[who("Grace Akello", "g.akello@snv.org", "GA", GREEN), "SNV", "SNV MEL Reviewer", "Now", ok(True)],
            [who("Brian Tumusiime", "brian.t@nrep.ug", "BT", LEARN), "NREP", "Partner MEL Focal Person", "2 h ago", ok(True)],
            [who("Sarah Nakato", "+256 772 ··· 418", "SN", AMBER_D), "NOGAMU", "Partner Field User", "Yesterday", ok(True)],
            [who("Regional MEL viewer", "Invitation sent 21 Sep", "RV", "#5B6770"), "SNV East Africa", "Read-only", "3 days ago", ok(False)]]
    table(s, X0 + 1, uy + 60, cols, rows, row_h=(uh - 60 - 36 - 8) / 4, head_h=36)

    px = X0 + lw + 20
    pw = X1 - px
    ph = H - 28 - y0
    with s.g("audit trail"):
        s.rect(px, y0, pw, ph, fill=CARD, rx=12, stroke=LINE)
        s.text(px + 24, y0 + 38, "Audit trail", 17, 600, INK)
        s.text(px + 24, y0 + 60, "Every entry, edit, approval and export — who, what, when", 13, 400, MUTED)
        s.text(px + pw - 24, y0 + 38, "Export log", 13, 600, GREEN, anchor="end")
        s.link(px, y0, pw, ph, "w17")
        events = [
            ("check", STATUS["Approved"], "Grace Akello approved 5 results", "NREP · Q3 technical report · v2", "10:42"),
            ("arrowleft", STATUS["Returned"], "Grace Akello returned OI 3.4", "Reason: meeting minutes missing", "10:40"),
            ("edit", LEARN, "Brian Tumusiime edited PHI 8", "620 → 1,020 · explanation added", "09:15"),
            ("refresh", "#5B6770", "System pushed 6 indicators to LogAlto", "1 conflict flagged (OI 3.1)", "02:04"),
            ("database", "#5B6770", "Daily backup completed", "1.24 GB · encrypted · checksum ok", "02:00"),
            ("upload", AMBER_D, "Sarah Nakato synced 38 records from phone", "Captured offline 22–23 Sep · Masaka", "Yesterday"),
            ("lock", STATUS["Rejected"], "3 failed sign-ins blocked", "unknown device · account locked 15 min", "Yesterday"),
            ("download", GREEN, "Grace Akello exported donor extract", "Q3 2026 · Excel · approved data only", "22 Sep"),
            ("users", "#5B6770", "Kenneth Mugisha role changed", "Partner Field User → Partner MEL Focal Person", "21 Sep"),
        ]
        y = y0 + 96
        step = (ph - 110) / len(events)
        for i, (ic, col, t1, t2, when) in enumerate(events):
            if i < len(events) - 1:
                s.line(px + 41, y + 34, px + 41, y + step, LINE, 2)
            s.circle(px + 41, y + 16, 16, fill=tint(col, 0.14))
            s.icon(ic, px + 33, y + 8, 16, col, 2.2)
            s.text(px + 70, y + 14, t1, 13.5, 600, INK, maxw=pw - 170)
            s.text(px + 70, y + 33, t2, 12.5, 400, MUTED, maxw=pw - 100)
            s.text(px + pw - 24, y + 14, when, 12, 400, MUTED, anchor="end")
            y += step
    return s


SCREENS = [w01_sign_in, w02_overview, w03_indicator, w04_partner_reporting, w05_report_review, w06_outcome_board,
           w07_outcome_detail, w08_signals, w09_gis, w10_partner_home, w11_report_form, w12_library, w13_logalto,
           w14_users]
