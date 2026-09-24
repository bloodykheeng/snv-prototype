# P4FP Uganda MEL Platform: presentation briefing

> **Internal · New Wave team only · do not share with SNV.**
> Everything you need to understand the assignment, speak the client's language, and show how the prototype answers what SNV will score.
>
> **Prototype:** https://snv-prototype.vercel.app. The screen links below open the right screen directly.

**Contents:** [1. 30-second version](#1-the-30-second-version) · [2. Words decoded](#2-the-words-they-will-use-decoded) · [3. The programme](#3-the-programme-in-facts) · [4. What SNV is buying](#4-what-snv-is-buying) · [5. MEL architecture](#5-p4fp-uganda-mel-architecture-what-they-mean) · [6. Data flow](#6-how-data-moves-through-the-system) · [7. Roles](#7-roles-tor-vs-our-proposal-vs-the-mockups) · [8. Scoring areas](#8-snvs-five-scoring-areas--what-to-show-and-say) · [9. Walkthrough script](#9-walkthrough-script-about-8-minutes) · [10. Likely questions](#10-likely-questions-and-short-answers) · [11. Watch-outs](#11-watch-outs-before-tomorrow)

---

## 1. The 30-second version

- **SNV** runs a programme called **Power for Food Partnership (P4FP)**, funded by the IKEA Foundation (2025–2029). In Uganda it helps farmers and small agribusinesses adopt **regenerative farming powered by renewable energy** (e.g. solar irrigation, solar dryers), working through **8 partner organisations** in **15 districts**.
- SNV needs a **MEL platform**: one system where partners report what they did and what changed, SNV checks and approves it, and approved results show on dashboards and maps and go to SNV's corporate system, **LogAlto**.
- They want it **live in 12 weeks**, then maintained until **December 2029**. We are at the **presentation stage**: we passed technical evaluation and now have to convince them in person.

---

## 2. The words they will use, decoded

| Term | What it means |
|---|---|
| **MEL** | **Monitoring, Evaluation and Learning.** Monitoring = tracking what's happening (numbers, activities). Evaluation = judging whether it worked. Learning = using the evidence to adjust the programme. A "MEL platform" is the software that holds all of this. |
| **MEL architecture** | How their measurement system is *structured*: which indicators, which methods, who reports what, how it rolls up. Our job is to turn that into software (section 5). |
| **Indicator** | A number tracked against a target, e.g. "farmers adopting RA-PURE practices: 18,420 of 45,000". |
| **Output vs outcome** | **Output** = what the programme delivered (people trained, solar units installed). **Outcome** = a change in how someone behaves or decides because of it (a district starts budgeting for solar irrigation). |
| **PHI** | A programme headline indicator. The ToR names **PHI 8** = farmer and agribusiness adoption of RA-PURE, linked to System Signal **SS5**. |
| **Outcome Harvesting** | A method for capturing outcomes *after* they happen: who changed what, when, where, why it matters, how we contributed. Then it's checked against evidence. Partners "harvest" outcomes; SNV verifies them. |
| **System Signals (SS1–SS8)** | Eight signs that the whole food-and-energy *system* is changing, not just individual farmers. SNV scores each **0–4** with a rubric and shows them on a **radar/spiderweb chart** over time. |
| **Rubric 0–4** | A scoring guide. Ours: 0 no signal · 1 emerging · 2 developing · 3 established · 4 embedded. Each score needs a written justification and linked outcomes. |
| **Sense Making / Pause & Reflect** | Periodic meetings where SNV and partners review evidence and agree the signal scores. The platform records them. |
| **LEARN · LINK · LEVERAGE** | The three pathways. **LEARN** = evidence and knowledge sharing · **LINK** = actors collaborating · **LEVERAGE** = policy, finance, investment. Every record is tagged with one. |
| **RA · PURE · nexus** | **RA** = Regenerative Agriculture (healthy soils, mulching, composting). **PURE** = Productive Use of Renewable Energy (solar pumps, dryers, mills). **Nexus** = treating both together. |
| **GESI · disaggregation** | **GESI** = Gender Equality and Social Inclusion. **Disaggregation** = splitting a number by sex, age, district or value chain (e.g. 54% of adopting farmers are women). |
| **Value chain** | A product and everything around it: coffee, dairy, horticulture, grains. |
| **LogAlto** | SNV's existing **corporate** M&E software. Our platform **complements** it and doesn't replace it. Approved figures flow to LogAlto by API, or as an Excel file if the API isn't available. |
| **Sub-grant** | Money SNV gives each partner in tranches. The ToR wants *high-level* milestone tracking (planned vs disbursed), not full accounting. |
| **Approval-gated** | Nothing counts in official dashboards, donor reports or LogAlto until SNV approves it. **The most important rule in the system.** |

---

## 3. The programme in facts

| What | Detail |
|---|---|
| **Programme** | Power for Food Partnership (P4FP), 2025–2029, in Uganda, Kenya, Rwanda and Ethiopia; funded by the IKEA Foundation |
| **Vision** | Renewable-energy-driven, resilient food systems where people have equitable opportunities to thrive |
| **8 partners** | ACSA (sustainable agriculture advocacy) · PELUM Uganda (ecological land use) · NREP (renewable energy platform) · ACME (media) · CREEC (energy research) · NOGAMU (organic agriculture) · NARO (agricultural research) · USEA (solar industry association) |
| **15 districts, 4 regions** | **Central:** Masaka, Mpigi, Mubende, Luwero, Nakasongola, Kayunga · **Western:** Mbarara, Kabarole, Isingiro, Kasese, Ntungamo · **Eastern:** Mbale, Iganga, Jinja · **Lango:** Lira |
| **Who we report to** | Systems Transformation / MEL Advisor (day to day); Programme Manager, P4FP Uganda (final approval) |

---

## 4. What SNV is buying

| Phase | What must happen | Payment |
|---|---|---|
| **Weeks 1–2** Inception | Requirements, data model, roles, wireframes, LogAlto approach → Inception Report | 30% |
| **Weeks 3–6** Design & prototype | UI/UX mock-ups, user journeys, workflows, prototype reviewed with SNV and partners | 30% |
| **Weeks 7–10** Build | Modules, mobile/offline, GIS, LogAlto link, security, staging environment | — |
| **Weeks 11–12** Test, train, go live | UAT, security and load tests, train all 8 partners, manuals, handover. **Must be in active use by week 12.** | 40% |
| **Week 13 → Dec 2029** Support | Fixes, security updates, user support, quarterly review reports. Paid quarterly *only* against support logs. | Quarterly |

> **Why it matters tomorrow:** the mockups you're showing are exactly what's due in weeks 3–6. Showing them now proves we understand the job before we're paid for it.

---

## 5. "P4FP Uganda MEL architecture": what they mean

It's the structure of how they measure change. There are five parts, and each has a home in our platform:

| Part of their MEL architecture | In plain words | Where it lives in the prototype |
|---|---|---|
| **Output indicators** (incl. PHI 8) | Numbers against targets, split by sex/age/district | [03 Indicator detail](https://snv-prototype.vercel.app/prototype.html#w03) · [02 Overview](https://snv-prototype.vercel.app/prototype.html#w02) |
| **Outcome Harvesting** | Stories of real change, backed by evidence | [06 Outcome board](https://snv-prototype.vercel.app/prototype.html#w06) · [07 Outcome review](https://snv-prototype.vercel.app/prototype.html#w07) · [M9 phone form](https://snv-prototype.vercel.app/prototype.html#m09) |
| **System Signals SS1–SS8** + rubric | Is the whole system shifting? Scored 0–4 | [08 System Signals](https://snv-prototype.vercel.app/prototype.html#w08) (radar over time) |
| **LEARN / LINK / LEVERAGE** | Every record tagged by pathway | Filters and tags on every screen; chart on [02](https://snv-prototype.vercel.app/prototype.html#w02) |
| **Partner reporting + geography** | 8 partners report quarterly; results mapped to 15 districts | [04 Compliance](https://snv-prototype.vercel.app/prototype.html#w04) · [11 Report form](https://snv-prototype.vercel.app/prototype.html#w11) · [09 GIS](https://snv-prototype.vercel.app/prototype.html#w09) |

> **One sentence to use:** "We don't treat this as a generic forms system. Your MEL framework (indicators, Outcome Harvesting, the eight System Signals and the three pathways) is the blueprint, and each part has its own screen and its own rules."

---

## 6. How data moves through the system

```
1 FIELD                2 PARTNER                   3 SNV REVIEW                 4 OFFICIAL USE
Field user on the  →   Partner MEL Focal Person →  SNV MEL Reviewer        →    Only approved data reaches
Android app: farmers,  checks, compiles the        approves / returns /         dashboards, maps, donor
GPS photos, outcomes   quarterly report, submits   rejects; system checks       reports, LogAlto and the
(works offline)        to SNV                      run automatically            public website
```

Every step is recorded in the [audit trail](https://snv-prototype.vercel.app/prototype.html#w17): who changed what, when, and the value before.

---

## 7. Roles: ToR vs our proposal vs the mockups

| ToR says (minimum) | Proposal & boss's deck | Mockups | Person shown | What they do |
|---|---|---|---|---|
| Super Administrator | Super Admin | Super Admin | (none named) | Manages users, permissions, settings |
| *(review sits with Super Admin / "SNV MEL Administrator")* | SNV MEL reviewer / approver | **SNV MEL Reviewer** | Grace Akello, SNV | Reviews, approves or returns partner data; scores System Signals |
| Partner MEL Focal Person | Partner MEL Focal | **Partner MEL Focal Person** | Brian Tumusiime, NREP | Enters and submits own partner's reports; sees own data only |
| Partner Field / Data Entry User | Field user | **Partner Field User** | Sarah Nakato, NOGAMU | Collects data in the field on the phone app; cannot submit to SNV |
| Read-Only User | Read-only stakeholder | **Read-only** | Regional MEL viewer | Views approved data (e.g. SNV regional/global teams) |

> **If asked "where does SNV MEL Reviewer come from?"** "The ToR lists the minimum roles. We split SNV's work into two: the Super Admin manages the system, the MEL Reviewer approves data. The person approving data shouldn't need to manage user accounts. It's all configurable at inception."
>
> **Job title ≠ system role.** Grace's job at SNV might be "MEL Advisor"; in the system she acts as *SNV MEL Reviewer*.

---

## 8. SNV's five scoring areas → what to show and say

### 1 · Clarity & understanding of the assignment: rationale, objectives, MEL architecture

**What they're checking:** do we understand *why* this platform is needed and *what* it must do, in their own terms?

- **Rationale (why):** past energy and agriculture projects were fragmented. P4FP's systems-change MEL (outcomes, signals, pathways) can't live in spreadsheets or in LogAlto alone. They need one layer where partners report and SNV reviews.
- **Objectives (what):** a live, secure platform in 12 weeks covering indicators, partner reporting, Outcome Harvesting, signal scoring, evidence, dashboards, GIS and LogAlto, then support to 2029.
- **Architecture:** section 5 above.

**Show:** [00 Landing page](https://snv-prototype.vercel.app/prototype.html#w00) (their programme in one view) → [02 Overview](https://snv-prototype.vercel.app/prototype.html#w02) (every part of the MEL architecture on one dashboard).

### 2 · Technical approach & live walkthrough

| They listed | Show | Point to make |
|---|---|---|
| System architecture | [13 LogAlto & exports](https://snv-prototype.vercel.app/prototype.html#w13) (flow diagram at top) | Partners → SNV review → platform → LogAlto; modular and API-ready |
| Demo / mockups | The whole prototype (section 9) | Illustrative; validated with SNV and partners in weeks 3–6 |
| Integrations / API | [13](https://snv-prototype.vercel.app/prototype.html#w13) | API if LogAlto allows, Excel import pack as fallback; conflicts flagged, not overwritten |
| Security | [01](https://snv-prototype.vercel.app/prototype.html#w01) → [01b](https://snv-prototype.vercel.app/prototype.html#w01b), [17 Audit trail](https://snv-prototype.vercel.app/prototype.html#w17) | Two-step login, encryption, tamper-evident audit log |
| GIS | [09 GIS & maps](https://snv-prototype.vercel.app/prototype.html#w09) | 15 real districts, partner areas, adoption hotspots, GPS points; admins can add districts |
| Dashboards & visualisation | [02](https://snv-prototype.vercel.app/prototype.html#w02), [08 radar](https://snv-prototype.vercel.app/prototype.html#w08) | Approved data only; programme view and partner view |
| Backups | [13](https://snv-prototype.vercel.app/prototype.html#w13) (Daily backups card) | Daily, encrypted, downloadable by SNV, restore tested |
| Mobile & field use | [M1–M13](https://snv-prototype.vercel.app/prototype.html#m01) | Android app (Flutter): offline, GPS, photos, sync with conflict handling |
| User roles & access | [14 Users & roles](https://snv-prototype.vercel.app/prototype.html#w14); switch to [10 NREP view](https://snv-prototype.vercel.app/prototype.html#w10) | Permissions = what you can do; scope = whose data you see |
| Maintenance & support | Boss's slide 11 | Severity levels, response times, quarterly review reports |

### 3 · Firm experience (evidence)

The closest match is the **Ministry of Public Service SDS tool**: the same pattern (standards → scoring → review → dashboards → map) across local governments. Plus MoWE water & sanitation M&E, and Palladium/UCIF (a donor-programme portal). **Have https://sdsbeta.nwtdemos.com open in a tab.** A live system beats slides.

### 4 · Workplan & risk mitigation

Boss's slides 10–11. Key lines: design and build overlap (coding starts week 3); only "Must-Have" modules are promised for week 12; LogAlto has an Excel fallback, so week 12 doesn't depend on an API we don't control.

### 5 · Budget alignment

Boss's slide 12. Every cost line should trace back to a module or requirement. **This slide currently has no figures** (see watch-outs).

---

## 9. Walkthrough script (about 8 minutes)

1. **[00 Landing page](https://snv-prototype.vercel.app/prototype.html#w00):** "The public face: approved, non-sensitive results only. This also meets the ToR's P4FP website requirement."
2. **[01 Sign in](https://snv-prototype.vercel.app/prototype.html#w01) → [01b Two-step code](https://snv-prototype.vercel.app/prototype.html#w01b):** "Secure login for SNV and partners."
3. **[02 Overview](https://snv-prototype.vercel.app/prototype.html#w02):** "SNV's management view. Indicators against targets, the eight signals, reach map, partner compliance. Note the 'approved data only' badge."
4. **[04 Partner reporting](https://snv-prototype.vercel.app/prototype.html#w04)** → click the NREP row → **[05 Review](https://snv-prototype.vercel.app/prototype.html#w05):** "The system checks data before SNV sees it: out-of-range values, duplicates, missing evidence. SNV approves or returns it. Every version is kept."
5. **[06 Outcome board](https://snv-prototype.vercel.app/prototype.html#w06)** → click the highlighted card → **[07](https://snv-prototype.vercel.app/prototype.html#w07):** "Outcome Harvesting: the statement, the evidence, and SNV mapping it to signals and a pathway."
6. **[08 System Signals](https://snv-prototype.vercel.app/prototype.html#w08):** "Sense Making: score 0–4, justify it, link outcomes, compare over time on the radar."
7. **[09 GIS](https://snv-prototype.vercel.app/prototype.html#w09):** "Where partners work, where adoption concentrates, where the gaps are."
8. Click Grace's name (bottom left) → **[10 NREP portal](https://snv-prototype.vercel.app/prototype.html#w10):** "The partner sees only their own data: due report, returned item, workplan, sub-grant."
9. Bottom bar → **Android app:** [splash](https://snv-prototype.vercel.app/prototype.html#m01) → sign in → [home (offline)](https://snv-prototype.vercel.app/prototype.html#m06) → [farmer record with GPS + duplicate check](https://snv-prototype.vercel.app/prototype.html#m07) → [sync](https://snv-prototype.vercel.app/prototype.html#m10).
10. **[17 Audit trail](https://snv-prototype.vercel.app/prototype.html#w17):** "Every change: who, when, before and after. Nobody can edit it."

---

## 10. Likely questions and short answers

**"What if LogAlto's API isn't available?"**
We agree the mechanism at inception. There's always an Excel import/export fallback, so week 12 doesn't depend on it.

**"How does it work with no internet in the field?"**
The Android app saves everything on the phone, including GPS and photos, and syncs when connected. Conflicts (e.g. the same farmer entered twice) are flagged for a person to resolve.

**"How do you stop double-counting farmers across partners?"**
Duplicate detection on phone number, name and village, across all partners, before submission ([screen 11](https://snv-prototype.vercel.app/prototype.html#w11)).

**"Can partners see each other's data?"**
No. Scope limits each partner to their own data unless SNV grants shared access. Sub-grant finance is restricted further.

**"Who owns the data and the code?"**
SNV owns all data, code and documentation. Source code sits in a repository SNV can access. Exports are available any time as CSV, Excel or PDF.

**"Is this system already built?"**
No. These are illustrative prototype screens with sample data, to show the workflow. The final design is validated with SNV and partners in weeks 3–6.

**"Why Flutter?"**
One codebase gives a real Android app with offline storage, GPS and camera, and it can extend to iPhone later without rebuilding. Open source, and SNV gets the code.

**"What are SS1–SS8 in your mockup?"**
The names on screen are placeholders. We'll load SNV's actual signal definitions and rubric at inception. SS5 = adoption (PHI 8) is from the ToR.

---

## 11. Watch-outs before tomorrow

**Fix or be ready for:**
1. **Budget slide has no numbers.** The ToR wants amounts in UGX with EUR equivalent: the 12-week total, the maximum per quarter for support, and hosting/recurring costs.
2. **PWA vs Flutter.** Deck slides 5, 8, 10, 12 and the proposal say PWA; slides 10 and 12 list a native app as an *optional extra*. If Flutter is core, update those slides and the budget.
3. **Names and years.** The MEL analyst is spelled Apanjo / Apajo / "Joseph Apajo" in different places; Eisah shows 16+ vs 18+ years. Pick one version.
4. **Draft notes in the submitted proposal** (e.g. "Confirm live demo access… before submission" for PPDA). Be ready if asked about the PPDA reference.

**On the day:**
5. **Say "illustrative" once** when you open the prototype: all names, figures and outcomes are sample data.
6. **Open the prototype while online** and wait for "✓ Offline-ready" in the bottom bar. Present in Chrome, full screen (**F**).
7. **Don't share this briefing with SNV.** It's internal. The prototype link is fine to share.

---

*Sources: SNV ToR, NWT technical proposal, NWT presentation deck v1, SNV invitation message.*
