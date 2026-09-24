"""Web screens added after the first review: evidence store and workplans & sub-grant milestones."""
from __future__ import annotations

from kit import (AMBER, AMBER_D, CARD, FAINT, GREEN, GREEN_D, INK, INK2, LEARN, LINE, LINE2, LINK, MUTED, STATUS,
                 button, card, chip, para, progress, status_chip, table, tint, tw)
from web import CW, H, X0, X1, Y0, filter_btn, page_head, shell

PARTNER_COL = {"ACSA": "#2E8B57", "PELUM Uganda": "#8E5BD6", "NREP": "#E0911A", "ACME": "#C2362F",
               "CREEC": "#2B6CB0", "NOGAMU": "#178A4C", "NARO": "#0F766E", "USEA": "#B7791F"}


def stat_tiles(s, y, tiles):
    n = len(tiles)
    tw_ = (CW - (n - 1) * 16) / n
    for i, (lab, val, sub, col) in enumerate(tiles):
        x = X0 + i * (tw_ + 16)
        with s.g(f"tile {lab}"):
            s.rect(x, y, tw_, 96, fill=CARD, rx=12, stroke=LINE)
            s.rect(x, y + 16, 4, 64, fill=col, rx=2)
            s.text(x + 22, y + 32, lab, 13, 600, INK2)
            s.text(x + 22, y + 70, val, 30, 700, INK)
            s.text(x + 30 + tw(val, 30, 700), y + 70, sub, 12.5, 400, MUTED)
    return tw_


# =====================================================================================
def w15_evidence():
    s = shell("15 Evidence store", "Evidence store", ["Knowledge", "Evidence store"])
    page_head(s, "Evidence store", "Every file behind a reported figure or outcome — who uploaded it, what it proves, "
                                   "where it was captured and whether SNV has verified it")
    x = X1
    x -= button(s, x, Y0 + 12, "Upload evidence", "primary", icon="upload", anchor="end") + 12
    button(s, x, Y0 + 12, "Export evidence register", "secondary", icon="download", anchor="end")

    ty = Y0 + 84
    tw_ = stat_tiles(s, ty, [("Files", "1,284", "all partners", LEARN), ("Verified", "1,041", "81%", STATUS["Approved"]),
                             ("Awaiting check", "157", "in review queue", STATUS["Under review"]),
                             ("Required but missing", "13", "blocking approval", STATUS["Returned"])])
    s.link(X0 + 3 * (tw_ + 16), ty, tw_, 96, "w04")

    ly = ty + 116
    lw = 1080
    lh = H - 28 - ly
    with s.g("evidence list"):
        s.rect(X0, ly, lw, lh, fill=CARD, rx=12, stroke=LINE)
        s.rect(X0 + 20, ly + 18, 300, 38, fill="#F4F6F3", rx=8, stroke=LINE)
        s.icon("search", X0 + 32, ly + 28, 18, MUTED)
        s.text(X0 + 58, ly + 42, "Search files, records, places", 13, 400, FAINT)
        fx = X0 + 334
        for lab, val in [("Type", "All"), ("Partner", "All"), ("Status", "All"), ("Access", "All")]:
            fx += filter_btn(s, fx, ly + 18, lab, val) + 10

        rows_data = [
            ("image", "Solar dryer demo – Kyanamukaka.jpg", "Photo · 2.1 MB", "Activity FFS-14", "NOGAMU", "Masaka", True, "Partner + SNV", "Pending"),
            ("file", "Adoption register – Isingiro & Mbarara.xlsx", "Register · 348 KB", "PHI 8 · NREP Q3", "NREP", "Isingiro", True, "Restricted", "Verified"),
            ("file", "District approved budget FY26/27 p.14.pdf", "Document · 1.2 MB", "Outcome OH-052", "NREP", "Mbarara", False, "Partner + SNV", "Verified"),
            ("image", "Budget conference – Mbarara (4 photos)", "Photos · 6.8 MB", "Outcome OH-052", "NREP", "Mbarara", True, "Public-ready", "Verified"),
            ("file", "Attendance – RA-PURE training Kabarole.pdf", "Attendance list · 540 KB", "OI 3.1 · PELUM Q3", "PELUM Uganda", "Kabarole", False, "Restricted", "Verified"),
            ("message", "Platform meeting minutes – Mbale", "Minutes · awaiting upload", "OI 3.4 · CREEC Q3", "CREEC", "Mbale", False, "Partner + SNV", "Missing"),
            ("coins", "Sub-grant expenditure summary Q3.xlsx", "Financial · 92 KB", "NREP financial Q3", "NREP", "—", False, "SNV finance only", "Pending"),
            ("mic", "Radio episode 7 – healthy soils.mp3", "Audio · 18 MB", "Knowledge product KP-031", "ACME", "Kasese", False, "Public-ready", "Verified"),
        ]
        cols = [("File", 390, "start"), ("Linked to", 190, "start"), ("Partner · place", 190, "start"),
                ("Access", 150, "start"), ("Status", lw - 920 - 2, "start")]
        rows = []
        for ic, name, meta, linked, partner, place, gps, access, st in rows_data:
            def fcell(s_, x, y, w, h, ic=ic, name=name, meta=meta, st=st):
                col = STATUS["Returned"] if st == "Missing" else GREEN
                s_.rect(x + 16, y + h / 2 - 18, 36, 36, fill=tint(col, 0.1), rx=8)
                s_.icon(ic, x + 25, y + h / 2 - 9, 18, col, 1.9)
                s_.text(x + 64, y + h / 2 - 2, name, 13.5, 600, INK, maxw=w - 76)
                s_.text(x + 64, y + h / 2 + 16, meta, 12, 400, MUTED)

            def lcell(s_, x, y, w, h, linked=linked):
                s_.icon("link", x + 16, y + h / 2 - 7, 14, LEARN, 2)
                s_.text(x + 36, y + h / 2 + 4.5, linked, 13, 400, INK, maxw=w - 44)

            def pcell(s_, x, y, w, h, partner=partner, place=place, gps=gps):
                s_.text(x + 16, y + h / 2 - 2, partner, 13, 600, INK)
                if gps:
                    s_.icon("pin", x + 16, y + h / 2 + 6, 13, STATUS["Approved"], 2)
                    s_.text(x + 33, y + h / 2 + 16, place + " · GPS", 12, 400, MUTED)
                else:
                    s_.text(x + 16, y + h / 2 + 16, place, 12, 400, MUTED)

            def acell(s_, x, y, w, h, access=access):
                restricted = access in ("Restricted", "SNV finance only")
                col = STATUS["Rejected"] if restricted else (STATUS["Published"] if access == "Public-ready" else MUTED)
                s_.icon("lock" if restricted else ("globe" if access == "Public-ready" else "users"), x + 16,
                        y + h / 2 - 8, 15, col, 2)
                s_.text(x + 38, y + h / 2 + 4.5, access, 12.5, 400, INK, maxw=w - 44)

            def scell(s_, x, y, w, h, st=st):
                m = {"Verified": "Approved", "Pending": "Under review", "Missing": "Overdue"}[st]
                from kit import chip as _chip
                _chip(s_, x + 16, y + h / 2 - 12, st, STATUS[m], dot=True)

            rows.append([fcell, lcell, pcell, acell, scell])
        table(s, X0 + 1, ly + 72, cols, rows, row_h=(lh - 72 - 40 - 8) / len(rows), head_h=40, hl=0)

    # ---- preview panel
    px = X0 + lw + 20
    pw = X1 - px
    with s.g("file preview"):
        s.rect(px, ly, pw, lh, fill=CARD, rx=12, stroke=LINE)
        # photo illustration
        iy = ly + 20
        ih = 250
        with s.g("photo"):
            s.rect(px + 20, iy, pw - 40, ih, fill="#8FB7D6", rx=10, name="sky")
            s.circle(px + pw - 90, iy + 60, 28, fill="#FFE39A", op=0.9)
            s.path(f"M{px + 20} {iy + 150} C {px + 150} {iy + 120}, {px + 300} {iy + 150}, {px + pw - 20} {iy + 118} "
                   f"L{px + pw - 20} {iy + ih - 10} Q{px + pw - 20} {iy + ih} {px + pw - 30} {iy + ih} "
                   f"L{px + 30} {iy + ih} Q{px + 20} {iy + ih} {px + 20} {iy + ih - 10} Z", fill="#6E9A4E")
            cx = px + pw / 2
            s.rect(cx - 90, iy + 86, 180, 84, fill="#1F3A5C", rx=4)
            s.rect(cx - 86, iy + 90, 172, 76, fill="#2E5B8F", rx=3)
            for k in range(1, 4):
                s.line(cx - 86 + k * 43, iy + 90, cx - 86 + k * 43, iy + 166, "#6B9BD1", 1)
            s.rect(cx - 104, iy + 184, 208, 34, fill="#7A4E2D", rx=4)
            s.rect(px + 32, iy + ih - 42, 250, 30, fill="#000000", op=0.55, rx=6)
            s.icon("pin", px + 40, iy + ih - 35, 16, "#FFB547", 2.2)
            s.text(px + 62, iy + ih - 22, "-0.3412, 31.7351 · ±5 m · 24 Sep 10:18", 11.5, 600, "#FFFFFF")
        y = iy + ih + 34
        s.text(px + 24, y, "Solar dryer demo – Kyanamukaka.jpg", 16, 600, INK, maxw=pw - 48)
        y += 22
        s.text(px + 24, y, "Uploaded from the field app by Sarah Nakato (NOGAMU) · synced 24 Sep 11:02", 12.5, 400,
               MUTED, maxw=pw - 48)
        y += 20
        for k, v, ok in [("GPS", "Captured on device · inside Masaka district", True),
                         ("Consent", "Recorded for 3 people in photo", True),
                         ("Integrity", "Original file kept · checksum stored", True),
                         ("Linked to", "Activity FFS-14 · PHI 8 adoption records (12)", True)]:
            y += 30
            s.icon("check", px + 24, y - 13, 16, STATUS["Approved"], 2.4)
            s.text(px + 48, y, k, 13, 600, INK)
            s.text(px + 140, y, v, 13, 400, INK2, maxw=pw - 164)
        y += 26
        s.line(px + 24, y, px + pw - 24, y, LINE)
        y += 26
        s.text(px + 24, y, "Who can see this file", 13, 600, INK2)
        y += 12
        opts = [("NOGAMU + SNV", True), ("All partners", False), ("Public website", False)]
        ow = (pw - 48 - 16) / 3
        for i, (lab, on) in enumerate(opts):
            ox = px + 24 + i * (ow + 8)
            s.rect(ox, y, ow, 36, fill=tint(GREEN, 0.1) if on else CARD, rx=8, stroke=GREEN if on else LINE)
            s.text(ox + ow / 2, y + 23, lab, 12.5, 600, GREEN_D if on else INK2, anchor="middle")
        y = ly + lh - 72
        s.line(px, y - 14, px + pw, y - 14, LINE)
        bw = (pw - 48 - 12) / 2
        button(s, px + 24, y, "Reject file", "danger", w=bw, h=44)
        button(s, px + 36 + bw, y, "Mark verified", "primary", icon="check", w=bw, h=44)
    return s


# =====================================================================================
WORKPLAN = [
    ("NREP", [("Solar pump demos · Mbarara", 1, 3.5, "On track"), ("District budget dialogues", 1.5, 2.6, "Complete"),
              ("Cold-chain feasibility study", 2, 5, "At risk")]),
    ("NOGAMU", [("Farmer field schools · Masaka", 0, 3, "Complete"), ("Organic certification support", 2, 5.5, "On track")]),
    ("CREEC", [("Solar maize mill pilots · Mbale", 0.5, 4, "Delayed"), ("PAYG pump business case", 2.5, 4.5, "On track")]),
    ("PELUM Uganda", [("RA curriculum with extension", 1, 4, "On track"), ("Kasese exchange visit", 3, 3.6, "On track")]),
    ("USEA", [("Dealer–SACCO finance workshops", 1, 2.8, "Delayed"), ("Solar dryer dealer network", 2, 5.3, "At risk")]),
]


def w16_workplans():
    s = shell("16 Workplans and sub-grant milestones", "Workplans & milestones", ["Partners", "Workplans & milestones"])
    page_head(s, "Workplans & sub-grant milestones", "Planned vs actual implementation for every partner, with "
                                                     "high-level financial milestones — Q3–Q4 2026")
    x = X1
    x -= button(s, x, Y0 + 12, "Export workplan status", "secondary", icon="download", anchor="end") + 12
    filter_btn(s, x - 180, Y0 + 13, "Partner", "All 8", w=180)

    ty = Y0 + 84
    stat_tiles(s, ty, [("Activities planned", "208", "this year", LEARN), ("Complete", "96", "46%", STATUS["Complete"]),
                       ("On track", "71", "34%", STATUS["On track"]), ("At risk", "28", "need follow-up", STATUS["At risk"]),
                       ("Delayed", "13", "past planned end", STATUS["Delayed"])])

    gy = ty + 116
    gw = 1030
    gh = H - 28 - gy
    card(s, X0, gy, gw, gh, "Activity timeline", "Bar = planned window · filled part = progress reported by the partner "
                                                 "· red line = today", action="All partners →")
    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    lx = X0 + 290
    lw_ = gw - 290 - 24
    with s.g("gantt"):
        for i, mth in enumerate(months):
            mx = lx + lw_ * i / 6
            s.rect(mx, gy + 84, lw_ / 6, 28, fill="#F7F9F6" if i % 2 == 0 else CARD)
            s.text(mx + lw_ / 12, gy + 103, mth, 12, 600, MUTED, anchor="middle")
        today = lx + lw_ * 2.8 / 6
        y = gy + 124
        rows = sum(len(a) + 1 for _, a in WORKPLAN)
        step = (gh - 124 - 16) / rows
        s.line(today, gy + 112, today, gy + gh - 16, STATUS["Overdue"], 1.6, dash="4 3")
        s.text(today + 6, gy + 124, "Today", 11.5, 600, STATUS["Overdue"])
        for partner, acts in WORKPLAN:
            s.rect(X0 + 24, y + step / 2 - 6, 12, 12, fill=PARTNER_COL[partner], rx=3)
            s.text(X0 + 44, y + step / 2 + 5, partner, 13.5, 700, INK)
            y += step
            for name, a, b, st in acts:
                col = STATUS[st]
                s.text(X0 + 44, y + step / 2 + 4.5, name, 13, 400, INK2, maxw=236)
                bx0 = lx + lw_ * a / 6
                bw = lw_ * (b - a) / 6
                s.rect(bx0, y + step / 2 - 9, bw, 18, fill=tint(col, 0.28), rx=5)
                done = 1 if st == "Complete" else min(max((2.8 - a) / (b - a), 0.05), 1) * (0.6 if st == "Delayed" else 1)
                s.rect(bx0, y + step / 2 - 9, bw * done, 18, fill=col, rx=5)
                if st in ("At risk", "Delayed"):
                    s.text(bx0 + bw + 8, y + step / 2 + 4.5, st, 11.5, 600, col)
                y += step

    rx = X0 + gw + 20
    rw = X1 - rx
    card(s, rx, gy, rw, gh, "Sub-grant milestones", "High-level financial tracking · restricted to SNV finance and MEL")
    s.icon("lock", rx + rw - 44, gy + 24, 18, MUTED, 2)
    y = gy + 96
    rows = [("NREP", "Tranche 3", 280, 184, "Submitted"), ("NOGAMU", "Tranche 3", 240, 168, "Approved"),
            ("PELUM Uganda", "Tranche 3", 260, 161, "Under review"), ("CREEC", "Tranche 2", 220, 110, "Returned"),
            ("ACSA", "Tranche 3", 180, 126, "Approved"), ("NARO", "Tranche 2", 300, 135, "Draft"),
            ("ACME", "Tranche 3", 150, 113, "Approved"), ("USEA", "Tranche 2", 200, 66, "Overdue")]
    step = (gh - 96 - 20) / len(rows)
    for p, tr, bud, dis, st in rows:
        s.text(rx + 24, y + 16, p, 13.5, 600, INK)
        s.text(rx + 24, y + 35, f"{tr} · UGX {dis}M of {bud}M", 12, 400, MUTED)
        progress(s, rx + 250, y + 20, rw - 250 - 160, dis / bud, GREEN if dis / bud > 0.5 else AMBER, h=8)
        status_chip(s, rx + rw - 24 - tw(st, 12, 600) - 34, y + 13, st)
        if p != "USEA":
            s.line(rx + 24, y + step - 6, rx + rw - 24, y + step - 6, LINE2)
        y += step
    return s


SCREENS = [w15_evidence, w16_workplans]
