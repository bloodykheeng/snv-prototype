# P4FP Uganda MEL Platform: presentation mockups

31 screens: 18 web (1920×1080) and 13 mobile field-app screens (360×800, installable on Android as a PWA). They are plain SVG, so Adobe XD imports them as editable shapes and text.

## Clickable prototype (use this for the live walkthrough)

Open `prototype.html` in Chrome. Press **F** or the Full screen button to go full screen, and **Esc** to leave it. The sidebar, key cards and buttons are all clickable (about 300 hotspots). Click empty space to flash where the hotspots are, press ← → to step through screens, and use **Web / Mobile field app (PWA)** in the bottom bar to switch. `prototype.html#w05` opens a specific screen directly.

Start-up flows:
- **Web:** public landing page (approved public results) → Sign in → two-step verification (OTP) → Programme overview. The red sign-out button next to the user's name in the sidebar returns to the landing page.
- **Mobile:** splash (moves on by itself) → Welcome → Sign in → SMS code (OTP) → Home. "Unlock with PIN" is for returning users. **Me** tab → Sign out → Welcome.

Main demo paths:
- Overview → Partner reporting → NREP row → Report review → Approve
- Overview → Outcomes card → Outcome board → highlighted Mbarara card → Outcome review
- Click the user's name at the bottom of the sidebar to switch between the SNV view and the NREP partner view (demo shortcut)
- Mobile: Home → Farmer adoption → Save offline → Sync queue; Home → Evidence photo → shutter

## Open them in Adobe XD

1. In XD, create an artboard (Web 1920 for web screens, or a custom 360×800 artboard for mobile).
2. Choose **File → Import** (Ctrl+Shift+I) and pick an SVG from `web/` or `mobile/`, or drag the file onto the artboard.
3. Every rectangle, icon and piece of text can be edited. Groups carry names (for example `kpi Farmers adopting RA-PURE`, `sidebar`, `radar chart`), so the Layers panel is readable.
4. The font is **Segoe UI**, which is already on Windows, so the text keeps its layout.

To show them without XD, open `index.html` in a browser (click a screen to see it full size) or use the PNGs in `_previews/`.

## Suggested walkthrough order (mapped to SNV's scoring areas)

| # | Screen | What to say | SNV scoring area |
|---|---|---|---|
| 1 | web/01 Sign in | Role-based access, Microsoft sign-in for SNV, two-step verification, Data Protection Act | Security, roles |
| 2 | web/02 Programme overview | SNV management view: approved data only, indicators vs target, SS1–SS8 radar, reach map, compliance | Dashboards and visualisation |
| 3 | web/03 Indicator detail | PHI 8 tracked with GESI disaggregation; the data dictionary and LogAlto code sit next to the figure | MEL architecture, understanding |
| 4 | web/10 Partner portal | NREP sees only its own data: due report, returned item, workplan, sub-grant tranche | Partner interface, access control |
| 5 | web/11 Report form | Validation, duplicate farmers across partners, evidence required, works offline | Data quality, field use |
| 6 | mobile/m2 → m3 → m4 → m6 | Field officer offline: register farmer with GPS, photo evidence, then sync with conflict handling | Mobile integration and field use |
| 7 | web/04 Partner reporting | Compliance view: submitted, overdue, returned, missing evidence, automatic reminders | Partner reporting |
| 8 | web/05 Report review | SNV approves or returns; checks run automatically; version history | Workflows, data governance |
| 9 | web/06 → web/07 Outcome harvesting | Pipeline board, then one outcome: evidence chain, mapped to signals and pathway | Outcome Harvesting |
| 10 | web/08 System Signals | Sense Making: 0–4 rubric, justification, linked outcomes, radar over time | Systems transformation |
| 11 | web/09 GIS | 15 districts / 4 regions, partner areas, adoption hotspots, GPS points, add-a-district | GIS |
| 12 | web/12 Knowledge library | Templates, tagging, review status, internal-only protection | Knowledge and comms |
| 13 | web/13 LogAlto & exports | API with Excel fallback, exports, daily downloadable backups, website feed | API integration, backups |
| 14 | web/14 Users & audit | Permission matrix (what) plus scope (whose), 2-step, full audit trail | Security, roles, maintenance |

## Before presenting, note

- **System Signal names are placeholders.** The ToR names SS1–SS8 but does not publish their titles (only that SS5 = adoption / PHI 8). Say so, or replace them from SNV's MEL framework.
- **All figures, people and outcomes are illustrative.** Indicator codes (OI x.x), LogAlto codes (SNV-AGR-03…) and partner operational areas are examples to confirm at inception.
- District boundaries are real (the UBOS boundaries also used in the SDS tool).

## Regenerating

The screens are generated from `_src/` (Python + Pillow). Edit the text or data there and run:

```
cd _src
python build.py          # rebuild all SVGs
python build.py --png    # also refresh PNG previews (uses Chrome)
python build.py w02 m3   # rebuild only matching screens
```
