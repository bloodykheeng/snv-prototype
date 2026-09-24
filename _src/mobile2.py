"""Mobile entry flow (splash, welcome, sign in, OTP) and the Me / profile screen."""
from __future__ import annotations

from kit import (AMBER, AMBER_D, CARD, FAINT, GREEN, GREEN_D, GREEN_M, INK, INK2, LEARN, LINE, LINE2, MUTED, STATUS,
                 avatar, button, chip, field, logo_mark, para, tint, toggle, tw)
from mobile import MH, MW, PAD, app_bar, bottom_nav, gesture_only, phone


def landscape(s, x, y, w, h, name="illustration"):
    """Sky, sun, crop rows and a small solar array — the programme in one picture."""
    with s.g(name):
        s.rect(x, y, w, h, fill="#DCEBE2", name="sky")
        s.circle(x + w * 0.72, y + h * 0.32, h * 0.16, fill=AMBER, name="sun")
        s.circle(x + w * 0.72, y + h * 0.32, h * 0.24, fill=AMBER, op=0.18, name="sun glow")
        s.path(f"M{x} {y + h * 0.62} C {x + w * 0.3} {y + h * 0.52}, {x + w * 0.6} {y + h * 0.66}, {x + w} {y + h * 0.55} "
               f"L{x + w} {y + h} L{x} {y + h} Z", fill="#7FAF6A", name="hill back")
        s.path(f"M{x} {y + h * 0.74} C {x + w * 0.35} {y + h * 0.66}, {x + w * 0.7} {y + h * 0.8}, {x + w} {y + h * 0.7} "
               f"L{x + w} {y + h} L{x} {y + h} Z", fill="#2F8F5E", name="field")
        for i in range(5):
            yy = y + h * (0.8 + i * 0.045)
            s.path(f"M{x} {yy:.1f} C {x + w * 0.35} {yy - h * 0.05:.1f}, {x + w * 0.7} {yy + h * 0.02:.1f}, {x + w} {yy - h * 0.05:.1f}",
                   stroke="#1E6B47", sw=3, sop=0.7, name=f"crop row {i + 1}")
        for k in range(3):
            px = x + w * 0.16 + k * w * 0.13
            py = y + h * 0.6
            s.rect(px, py, w * 0.11, h * 0.1, fill="#1F3A5C", rx=2, name=f"panel {k + 1}")
            s.rect(px + 2, py + 2, w * 0.11 - 4, h * 0.1 - 4, fill="#2E5B8F", rx=1.5)
            s.line(px + w * 0.055, py + 2, px + w * 0.055, py + h * 0.1 - 2, "#6B9BD1", 1)
            s.rect(px + w * 0.05, py + h * 0.1, 3, h * 0.06, fill="#1F3A5C")


def keypad(s, y0, target):
    keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "", "0", "del"]
    kw, kh = 96, 52
    x0 = (MW - 3 * kw - 2 * 12) / 2
    with s.g("keypad"):
        for i, k in enumerate(keys):
            cx = x0 + (i % 3) * (kw + 12)
            cy = y0 + (i // 3) * (kh + 8)
            if k == "del":
                s.icon("arrowleft", cx + kw / 2 - 11, cy + kh / 2 - 11, 22, INK2, 2)
            elif k:
                s.rect(cx, cy, kw, kh, fill="#F3F6F2", rx=12, name=f"key {k}")
                s.text(cx + kw / 2, cy + kh / 2 + 8, k, 22, 400, INK, anchor="middle")
    s.link(0, y0, MW, 4 * (kh + 8), target)


# =====================================================================================
def m01_splash():
    s = phone("M1 Splash", bg=GREEN_D, dark_status=True)
    with s.g("brand"):
        s.circle(MW / 2, 330, 120, fill="#FFFFFF", op=0.04)
        s.circle(MW / 2, 330, 84, fill="#FFFFFF", op=0.06)
        logo_mark(s, MW / 2 - 44, 286, 88)
        s.text(MW / 2, 470, "P4FP MEL", 30, 700, "#FFFFFF", anchor="middle")
        s.text(MW / 2, 498, "Field app", 16, 400, "#CFE3D7", anchor="middle")
    with s.g("loading dots"):
        for i in range(3):
            s.circle(MW / 2 - 16 + i * 16, 590, 4, fill=AMBER if i == 1 else "#FFFFFF", op=None if i == 1 else 0.4)
    s.text(MW / 2, 730, "SNV · Power for Food Partnership Uganda", 12, 400, "#A9C9B5", anchor="middle")
    s.text(MW / 2, 750, "Funded by the IKEA Foundation", 11.5, 400, "#7FA58F", anchor="middle")
    s.link(0, 0, MW, MH, "m02")
    gesture_only(s, dark=True)
    return s


def m02_welcome():
    s = phone("M2 Welcome", bg=CARD)
    landscape(s, 0, 24, MW, 360)
    with s.g("copy"):
        s.text(PAD + 4, 432, "Report from the field —", 23, 700, INK)
        s.text(PAD + 4, 462, "even without internet", 23, 700, GREEN)
        para(s, PAD + 4, 496, "Register farmers, capture GPS-stamped evidence and harvest outcomes. Everything saves on "
                              "your phone and syncs when you are back online.", MW - 2 * PAD - 8, 14, 400, INK2, lh=21)
    with s.g("pager"):
        s.rect(PAD + 4, 580, 22, 6, fill=GREEN, rx=3)
        s.circle(PAD + 38, 583, 3, fill="#C5CCC7")
        s.circle(PAD + 50, 583, 3, fill="#C5CCC7")
    button(s, PAD, 640, "Sign in", "primary", w=MW - 2 * PAD, h=50, size=15)
    s.link(PAD, 640, MW - 2 * PAD, 50, "m03")
    button(s, PAD, 700, "Unlock with PIN on this phone", "ghost", icon="lock", w=MW - 2 * PAD, h=44, size=13.5)
    s.link(PAD, 700, MW - 2 * PAD, 44, "m05")
    gesture_only(s)
    return s


def m03_sign_in():
    s = phone("M3 Sign in", bg=CARD)
    s.icon("arrowleft", PAD, 40, 24, INK, 2)
    s.link(0, 24, 56, 56, "m02")
    logo_mark(s, PAD, 100, 44)
    s.text(PAD, 186, "Sign in", 26, 700, INK)
    s.text(PAD, 212, "Use the account your MEL focal person set up.", 14, 400, MUTED)
    y = 240
    y += field(s, PAD, y, MW - 2 * PAD, "Email or phone", "sarah.nakato@nogamu.org.ug", h=50, icon="user", size=14.5) + 14
    y += field(s, PAD, y, MW - 2 * PAD, "Password", "••••••••••", h=50, icon="lock", size=15) + 8
    s.text(MW - PAD, y + 8, "Forgot password?", 13.5, 600, GREEN, anchor="end")
    y += 36
    button(s, PAD, y, "Continue", "primary", w=MW - 2 * PAD, h=50, size=15)
    s.link(PAD, y, MW - 2 * PAD, 50, "m04")
    y += 74
    with s.g("divider"):
        s.line(PAD, y, MW / 2 - 20, y, LINE)
        s.text(MW / 2, y + 5, "or", 12.5, 400, MUTED, anchor="middle")
        s.line(MW / 2 + 20, y, MW - PAD, y, LINE)
    y += 24
    button(s, PAD, y, "SNV staff: Microsoft account", "secondary", icon="sparkle", w=MW - 2 * PAD, h=48, size=13.5)
    s.link(PAD, y, MW - 2 * PAD, 48, "m04")
    with s.g("security note"):
        s.rect(PAD, 690, MW - 2 * PAD, 58, fill="#F4F7F3", rx=12)
        s.icon("shield", PAD + 14, 707, 22, GREEN, 2)
        para(s, PAD + 48, 714, "Your data is encrypted on the phone and in transit.", MW - 2 * PAD - 60, 12.5, 400, INK2,
             lh=18)
    gesture_only(s)
    return s


def m04_otp():
    s = phone("M4 One-time code", bg=CARD)
    s.icon("arrowleft", PAD, 40, 24, INK, 2)
    s.link(0, 24, 56, 56, "m03")
    s.rect(PAD, 100, 48, 48, fill=tint(GREEN, 0.12), rx=12)
    s.icon("message", PAD + 12, 112, 24, GREEN, 2)
    s.text(PAD, 190, "Check your phone", 24, 700, INK)
    para(s, PAD, 218, "We sent a 6-digit code by SMS to +256 772 ··· 418. It expires in 5 minutes.", MW - 2 * PAD, 14,
         400, MUTED, lh=21)
    with s.g("code boxes"):
        bw = (MW - 2 * PAD - 5 * 8) / 6
        for i, d in enumerate("4823"):
            pass
        for i in range(6):
            x = PAD + i * (bw + 8)
            filled = i < 4
            s.rect(x, 272, bw, 56, fill=CARD, rx=10, stroke=GREEN if i == 4 else ("#CFD6D1" if not filled else INK2),
                   sw=2 if i == 4 else 1.2)
            if filled:
                s.text(x + bw / 2, 309, "4823"[i], 24, 600, INK, anchor="middle")
            if i == 4:
                s.rect(x + bw / 2 - 1, 288, 2, 24, fill=GREEN)
    s.text(PAD, 360, "Didn't get it?", 13.5, 400, MUTED)
    s.text(PAD + tw("Didn't get it?", 13.5) + 6, 360, "Resend in 0:42", 13.5, 600, INK2)
    keypad(s, 392, "m06")
    s.text(MW / 2, 660, "Next you'll set a PIN so the app opens offline.", 12.5, 400, MUTED, anchor="middle")
    button(s, PAD, 690, "Verify", "primary", w=MW - 2 * PAD, h=50, size=15)
    s.link(PAD, 690, MW - 2 * PAD, 50, "m06")
    gesture_only(s)
    return s


def m13_profile():
    s = phone("M13 Me and sign out")
    app_bar(s, "Me", back=False)
    with s.g("profile card"):
        s.rect(PAD, 96, MW - 2 * PAD, 104, fill=CARD, rx=14, stroke=LINE)
        avatar(s, PAD + 44, 142, 28, "SN", AMBER_D)
        s.text(PAD + 84, 134, "Sarah Nakato", 17, 700, INK)
        s.text(PAD + 84, 154, "NOGAMU · Masaka & Mpigi", 12.5, 400, MUTED)
        chip(s, PAD + 84, 166, "Partner Field User", LEARN, h=22, size=11)
    y = 212
    sections = [
        ("OFFLINE & SYNC", [("refresh", "Last synced", "Today 11:02", None), ("database", "Stored on phone", "38 MB · 7 unsynced", None),
                            ("wifi", "Sync on Wi-Fi only", None, False)]),
        ("SECURITY", [("lock", "Change PIN", None, None), ("fingerprint", "Unlock with fingerprint", None, True)]),
        ("HELP", [("book", "User guide & training videos", None, None), ("message", "Contact support", "NWT help desk", None)]),
    ]
    for title, rows in sections:
        s.text(PAD, y + 12, title, 11, 600, FAINT, spacing=1)
        y += 22
        h = len(rows) * 44
        s.rect(PAD, y, MW - 2 * PAD, h, fill=CARD, rx=12, stroke=LINE)
        for i, (ic, lab, val, tog) in enumerate(rows):
            ry = y + i * 44
            if i:
                s.line(PAD + 48, ry, MW - PAD, ry, LINE2)
            s.icon(ic, PAD + 14, ry + 12, 20, INK2, 1.9)
            s.text(PAD + 48, ry + 27, lab, 14, 400, INK)
            if tog is not None:
                toggle(s, MW - PAD - 50, ry + 12, tog)
            else:
                if val:
                    s.text(MW - PAD - 34, ry + 27, val, 12.5, 400, MUTED, anchor="end")
                s.icon("chevright", MW - PAD - 30, ry + 13, 18, FAINT)
        y += h + 12
    with s.g("sign out"):
        s.rect(PAD, y + 2, MW - 2 * PAD, 48, fill=CARD, rx=12, stroke=tint(STATUS["Rejected"], 0.45))
        s.icon("logout", MW / 2 - 44, y + 16, 20, STATUS["Rejected"], 2)
        s.text(MW / 2 - 16, y + 31, "Sign out", 14.5, 600, STATUS["Rejected"])
        s.link(PAD, y + 2, MW - 2 * PAD, 48, "m02")
        s.text(MW / 2, y + 70, "7 records will sync before you sign out · v1.0.0", 11.5, 400, MUTED, anchor="middle")
    bottom_nav(s, "Me")
    return s


FIRST = [m01_splash, m02_welcome, m03_sign_in, m04_otp]
LAST = [m13_profile]
