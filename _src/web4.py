"""Audit trail, and the partner (NREP) versions of screens so a partner never lands in the SNV view."""
from __future__ import annotations

import web
from kit import (AMBER, AMBER_D, CARD, FAINT, GREEN, GREEN_D, INK, INK2, LEARN, LINE, LINE2, LINK, MUTED, PATHWAY,
                 STATUS, avatar, button, card, chip, para, progress, status_chip, table, tint, tw)
from web import CW, H, NAV_PARTNER, PARTNER_USER, X0, X1, Y0, filter_btn, page_head, shell
from web2 import stat_tiles

ACTION = {"Approved": STATUS["Approved"], "Returned": STATUS["Returned"], "Edited": LEARN, "Created": "#0F766E",
          "Deleted": STATUS["Rejected"], "Exported": GREEN, "Synced": AMBER_D, "Signed in": "#5B6770",
          "Sign-in blocked": STATUS["Rejected"], "Role changed": LINK, "Scored": LINK}


# =====================================================================================
def w17_audit():
    s = shell("17 Audit trail", "Audit trail", ["Administration", "Audit trail"])
    page_head(s, "Audit trail", "Every entry, edit, deletion, approval, return, export and sign-in — who, when, from "
                                "where, and what changed. Read-only: nobody can edit or delete it.")
    x = X1
    x -= button(s, x, Y0 + 12, "Export log (CSV / PDF)", "primary", icon="download", anchor="end") + 12
    filter_btn(s, x - 250, Y0 + 13, "Dates", "1 – 24 Sep 2026", w=250)

    fy = Y0 + 84
    with s.g("filters"):
        s.rect(X0, fy, 340, 40, fill=CARD, rx=8, stroke=LINE)
        s.icon("search", X0 + 12, fy + 11, 18, MUTED)
        s.text(X0 + 40, fy + 25, "Search user, record or ID", 13, 400, FAINT)
        fx = X0 + 356
        for lab, val in [("User", "All"), ("Action", "All"), ("Module", "All"), ("Partner", "All")]:
            fx += filter_btn(s, fx, fy + 1, lab, val) + 10
        s.text(X1, fy + 26, "2,418 events in this range", 13, 400, MUTED, anchor="end")

    ty = fy + 60
    lw = 1080
    th = H - 28 - ty
    events = [
        ("24 Sep 10:42", "Grace Akello", "GA", GREEN, "SNV MEL Reviewer", "Approved", "NREP · Q3 technical report", "5 of 6 results"),
        ("24 Sep 10:40", "Grace Akello", "GA", GREEN, "SNV MEL Reviewer", "Returned", "OI 3.4 · NREP Q3", "Minutes missing"),
        ("24 Sep 09:15", "Brian Tumusiime", "BT", LEARN, "Partner MEL Focal Person", "Edited", "PHI 8 · NREP Q3", "620 → 1,020"),
        ("24 Sep 02:04", "System", "SY", "#5B6770", "Scheduled job", "Synced", "LogAlto push", "6 indicators · 1 conflict"),
        ("23 Sep 18:22", "Sarah Nakato", "SN", AMBER_D, "Partner Field User", "Created", "38 adoption records", "Offline · Masaka"),
        ("23 Sep 16:05", "Unknown device", "!", STATUS["Rejected"], "—", "Sign-in blocked", "brian.t@nrep.ug", "3 failed attempts"),
        ("22 Sep 14:31", "Grace Akello", "GA", GREEN, "SNV MEL Reviewer", "Exported", "Donor extract Q3", "Approved data only"),
        ("21 Sep 11:10", "Super Admin", "SA", "#5B6770", "Super Admin", "Role changed", "Kenneth Mugisha", "Field User → MEL Focal Person"),
        ("20 Sep 15:48", "Peter Okello", "PO", LINK, "Partner MEL Focal Person", "Deleted", "Draft photo (duplicate)", "Kept in history"),
        ("16 Sep 17:02", "Grace Akello", "GA", GREEN, "SNV MEL Reviewer", "Scored", "SS2 Actor collaboration", "2.5 → 3.0"),
    ]
    cols = [("Time", 130, "start"), ("User", 250, "start"), ("Action", 160, "start"), ("Record", 250, "start"),
            ("Detail", lw - 790 - 2, "start")]
    rows = []
    for when, who, ini, col, role, act, rec, det in events:
        def ucell(s_, x, y, w, h, who=who, ini=ini, col=col, role=role):
            avatar(s_, x + 30, y + h / 2, 14, ini, col)
            s_.text(x + 52, y + h / 2 - 2, who, 13.5, 600, INK)
            s_.text(x + 52, y + h / 2 + 15, role, 12, 400, MUTED)

        def acell(s_, x, y, w, h, act=act):
            chip(s_, x + 16, y + h / 2 - 12, act, ACTION[act], dot=True)

        rows.append([when, ucell, acell, rec, det])
    with s.g("audit table card"):
        s.rect(X0, ty, lw, th, fill=CARD, rx=12, stroke=LINE)
        table(s, X0 + 1, ty + 1, cols, rows, row_h=(th - 44) / len(rows), head_h=40, hl=2)

    # ---- event detail
    px = X0 + lw + 20
    pw = X1 - px
    with s.g("event detail"):
        s.rect(px, ty, pw, th, fill=CARD, rx=12, stroke=LINE)
        chip(s, px + 24, ty + 22, "Edited", ACTION["Edited"], dot=True)
        s.text(px + pw - 24, ty + 39, "Event #A-20931", 12.5, 600, MUTED, anchor="end")
        s.text(px + 24, ty + 86, "PHI 8 value changed in NREP Q3 report", 18, 700, INK, maxw=pw - 48)
        s.text(px + 24, ty + 110, "Brian Tumusiime · Partner MEL Focal Person · 24 Sep 2026, 09:15:42", 13, 400, MUTED)
        y = ty + 140
        s.text(px + 24, y, "What changed", 13, 600, INK2)
        y += 12
        for field, before, after in [("Farmers adopting (total)", "620", "1,020"), ("Women 18–35", "130", "214"),
                                     ("Explanation", "—", "Two new clusters in Isingiro…")]:
            s.rect(px + 24, y, pw - 48, 46, fill="#F7F9F6", rx=8)
            s.text(px + 38, y + 28, field, 13, 600, INK, maxw=170)
            bx = px + 220
            s.text(bx, y + 28, before, 13, 400, STATUS["Rejected"], maxw=80)
            s.line(bx, y + 24, bx + tw(before, 13), y + 24, STATUS["Rejected"], 1)
            s.icon("arrowright", bx + 90, y + 15, 16, MUTED, 2)
            s.text(bx + 116, y + 28, after, 13, 600, STATUS["Approved"], maxw=pw - 48 - 330)
            y += 54
        y += 12
        s.text(px + 24, y, "Context", 13, 600, INK2)
        y += 8
        for k, v in [("Version", "v1 → v2 of the report (both kept)"), ("Device", "Chrome · Windows · Kampala"),
                     ("IP address", "41.210.x.x (masked)"), ("Session", "Signed in 08:52 with two-step code"),
                     ("Next step", "Approved by Grace Akello at 10:42")]:
            y += 30
            s.text(px + 24, y, k, 12.5, 400, MUTED)
            s.text(px + 130, y, v, 13, 400, INK, maxw=pw - 154)
        y = ty + th - 104
        s.rect(px + 24, y, pw - 48, 80, fill=tint(GREEN, 0.07), rx=10)
        s.icon("shield", px + 40, y + 16, 20, GREEN, 2)
        s.text(px + 70, y + 31, "Tamper-evident log", 13.5, 600, INK)
        para(s, px + 70, y + 52, "Each entry is chained to the one before it, so any change would show. Kept to "
                                 "December 2029 and exportable at any time.", pw - 110, 12, 400, INK2, lh=17)
    return s


# =====================================================================================
NREP_IND = [
    ("PHI 8", "Farmers adopting RA-PURE practices", 9000, 3940, "1,020", "Under review", 3),
    ("OI 1.2", "Hectares under regenerative practices", 3000, 1310, "240 ha", "Approved", 2),
    ("OI 2.1", "Agribusinesses using PURE solutions", 120, 64, "18", "Approved", 2),
    ("OI 2.3", "Solar irrigation & processing units", 800, 388, "74", "Approved", 4),
    ("OI 3.1", "People trained on RA-PURE", 6000, 3410, "640", "Approved", 2),
    ("OI 3.4", "Multi-actor platforms active", 6, 3, "3", "Returned", 0),
    ("OI 4.1", "Policy engagements with evidence", 12, 3, "2", "Approved", 1),
    ("OI 4.2", "Finance mobilised (EUR, thousands)", 1000, 210, "29", "Submitted", 1),
    ("OI 4.3", "Organisational capacity score", 4, 2.6, "—", "Not due", 0),
]


def w10b_partner_indicators():
    s = shell("10b My indicators (NREP)", "Indicators", ["NREP", "Indicators"], user=PARTNER_USER, nav=NAV_PARTNER)
    page_head(s, "My indicators", "NREP's 9 indicators · Q3 2026 values you submitted and what SNV has approved. "
                                  "You only see NREP figures.")
    button(s, X1, Y0 + 12, "Export NREP data", "secondary", icon="download", anchor="end")
    ty = Y0 + 84
    stat_tiles(s, ty, [("On track", "7 of 9", "indicators", STATUS["Approved"]),
                       ("Awaiting SNV", "2", "values under review", STATUS["Under review"]),
                       ("Returned", "1", "needs evidence", STATUS["Returned"]),
                       ("Evidence files", "15", "linked this quarter", LEARN)])
    cy = ty + 116
    ch = H - 28 - cy
    cols = [("Indicator", 460, "start"), ("Achieved (approved)", 360, "start"), ("Q3 submitted", 170, "end"),
            ("Q3 status", 200, "start"), ("Evidence", 140, "start"), ("", CW - 1330 - 2, "end")]
    rows = []
    for code, name, tgt, got, q3, st, ev in NREP_IND:
        fr = got / tgt

        def icell(s_, x, y, w, h, code=code, name=name):
            s_.text(x + 16, y + h / 2 - 2, name, 14, 600, INK)
            s_.text(x + 16, y + h / 2 + 16, code, 12, 400, MUTED)

        def pcell(s_, x, y, w, h, fr=fr, got=got, tgt=tgt):
            progress(s_, x + 16, y + h / 2 - 4, 170, fr, GREEN if fr >= 0.4 else AMBER, h=8)
            fmt = (lambda v: f"{v:,.1f}" if isinstance(v, float) else f"{v:,}")
            s_.text(x + 200, y + h / 2 + 4.5, f"{fmt(got)} / {fmt(tgt)}", 13, 600, INK)

        def scell(s_, x, y, w, h, st=st):
            status_chip(s_, x + 16, y + h / 2 - 12, st)

        def ecell(s_, x, y, w, h, ev=ev, st=st):
            col = STATUS["Returned"] if ev == 0 and st == "Returned" else (FAINT if ev == 0 else GREEN)
            s_.icon("clip", x + 16, y + h / 2 - 8, 16, col, 2)
            s_.text(x + 38, y + h / 2 + 4.5, f"{ev} file{'s' if ev != 1 else ''}", 13, 400, INK)

        def act(s_, x, y, w, h, st=st):
            if st == "Returned":
                button(s_, x + w - 16, y + h / 2 - 16, "Add evidence", "danger", anchor="end", h=32, size=13)
            else:
                s_.icon("chevright", x + w - 36, y + h / 2 - 10, 20, FAINT)

        rows.append([icell, pcell, q3, scell, ecell, act])
    with s.g("indicator table card"):
        s.rect(X0, cy, CW, ch, fill=CARD, rx=12, stroke=LINE)
        table(s, X0 + 1, cy + 1, cols, rows, row_h=(ch - 44) / len(rows), head_h=40, hl=5)
    return s


NREP_OUT = [
    ("Isingiro dairy cooperative adopted solar milk chilling, cutting spoilage losses", ["SS5", "SS6"], "LINK", "Returned", "20 Sep"),
    ("Mbarara District allocated UGX 120M in its FY26/27 budget for solar irrigation demonstration sites", ["SS3", "SS4"], "LEVERAGE", "Under review", "16 Sep"),
    ("Ntungamo farmer groups began sharing solar pumps on a rota", ["SS2", "SS5"], "LINK", "Submitted", "22 Sep"),
    ("Lira dealers stocked PURE-ready irrigation kits for the first time", ["SS6"], "LINK", "Draft", "23 Sep"),
    ("MEMD included productive use of solar in agriculture in the draft energy policy review", ["SS3"], "LEVERAGE", "Approved", "02 Sep"),
    ("Isingiro women's groups negotiated reserved time on solar irrigation schemes", ["SS8", "SS5"], "LINK", "Approved", "18 Aug"),
    ("Mbarara production office now co-hosts RA-PURE demonstrations", ["SS7"], "LEARN", "Approved", "30 Jul"),
]


def w10c_partner_outcomes():
    s = shell("10c My outcomes (NREP)", "Outcomes", ["NREP", "Outcomes"], user=PARTNER_USER, nav=NAV_PARTNER)
    page_head(s, "My outcomes", "Outcomes NREP has harvested. SNV categorises and approves them before they count "
                                "towards System Signals.")
    button(s, X1, Y0 + 12, "Harvest an outcome", "primary", icon="plus", anchor="end")
    ty = Y0 + 84
    stat_tiles(s, ty, [("Draft", "1", "not sent", STATUS["Draft"]), ("Submitted", "1", "to SNV", STATUS["Submitted"]),
                       ("Under review", "2", "with SNV MEL", STATUS["Under review"]),
                       ("Returned", "1", "needs your action", STATUS["Returned"]),
                       ("Approved", "12", "counted", STATUS["Approved"])])
    cy = ty + 116
    with s.g("returned banner"):
        s.rect(X0, cy, CW, 96, fill=tint(STATUS["Returned"], 0.07), rx=12, stroke=tint(STATUS["Returned"], 0.4))
        s.icon("arrowleft", X0 + 22, cy + 22, 20, STATUS["Returned"], 2.2)
        s.text(X0 + 54, cy + 36, "Returned by SNV: “Isingiro dairy cooperative adopted solar milk chilling…”", 15, 600, INK)
        avatar(s, X0 + 66, cy + 66, 12, "GA", GREEN)
        s.text(X0 + 86, cy + 71, "Grace Akello: please add the cooperative's before/after spoilage records as evidence, "
                                 "then resubmit.", 13, 400, INK2)
        button(s, X1 - 24, cy + 28, "Fix and resubmit", "danger", icon="edit", anchor="end", h=40)
    ly = cy + 116
    lh = H - 28 - ly
    cols = [("Outcome statement", 760, "start"), ("Signals", 190, "start"), ("Pathway", 150, "start"),
            ("Status", 190, "start"), ("Updated", CW - 1290 - 2, "start")]
    rows = []
    for stmt, sigs, pw_, st, d in NREP_OUT:
        def sc(s_, x, y, w, h, sigs=sigs):
            xx = x + 16
            for sg in sigs:
                xx += chip(s_, xx, y + h / 2 - 11, sg, "#5B6770", h=22, size=11) + 6

        def pc(s_, x, y, w, h, pw_=pw_):
            chip(s_, x + 16, y + h / 2 - 11, pw_, PATHWAY[pw_], h=22, size=11)

        def stc(s_, x, y, w, h, st=st):
            status_chip(s_, x + 16, y + h / 2 - 12, st)

        rows.append([stmt, sc, pc, stc, d])
    with s.g("outcome list"):
        s.rect(X0, ly, CW, lh, fill=CARD, rx=12, stroke=LINE)
        table(s, X0 + 1, ly + 1, cols, rows, row_h=(lh - 44) / len(rows), head_h=40, size=13.5, hl=0)
    return s


# partner-shell versions of shared screens --------------------------------------------
def _as_partner(fn, title):
    web.PARTNER_MODE["on"] = True
    try:
        s = fn()
    finally:
        web.PARTNER_MODE["on"] = False
    s.title = title
    return s


def w12p_library_partner():
    return _as_partner(web.w12_library, "12p Knowledge library (NREP view)")


def w09p_map_partner():
    return _as_partner(web.w09_gis, "09p Programme map (NREP view)")


SCREENS = [w10b_partner_indicators, w10c_partner_outcomes, w12p_library_partner, w09p_map_partner, w17_audit]
