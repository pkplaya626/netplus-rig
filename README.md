# 🚀 CompTIA Network+ (N10-009) 30-Day Training Rig & Telemetry Engine

[![Daily Telemetry Proctor](https://github.com/OWNER/netplus-rig/actions/workflows/telemetry-audit.yml/badge.svg)](https://github.com/OWNER/netplus-rig/actions/workflows/telemetry-audit.yml)
[![Pages Deployment](https://github.com/OWNER/netplus-rig/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/OWNER/netplus-rig/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated, serverless, GitHub-native training rig enforcing a strict 30-day CompTIA Network+ (N10-009) certification sprint. Runs entirely client-side on GitHub Pages and utilizes GitHub Actions as an automated 23:59 proctor.

---

<!-- START_AUTOGEN_DASHBOARD -->
### 📡 Live Sprint Telemetry Dashboard
*Sprint Start: **2026-09-23** | First Deadline: **Tomorrow (2026-09-23) at 23:59 EDT***  
*Last Proctor Sync: `2026-09-26 08:51 UTC` | Current Day: **Day 04 of 30***

```text
+-------------------------------------------------------------------------------+
|  STREAK: 00 DAYS ACTIVE (RECORD: 01)  |  CARDS: 100 SEEDED  |  QUESTIONS: 41 POOL  |
+-------------------------------------------------------------------------------+
```

#### 🗓️ 30-Day Sprint Calendar Matrix
| Week | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **W1** | 🟩 D01 | 🟥 D02 | 🟥 D03 | 🟥 D04 | ⬜ D05 | ⬜ D06 |
| **W2** | ⬜ D07 | ⬜ D08 | ⬜ D09 | ⬜ D10 | ⬜ D11 | ⬜ D12 |
| **W3** | ⬜ D13 | ⬜ D14 | ⬜ D15 | ⬜ D16 | ⬜ D17 | ⬜ D18 |
| **W4** | ⬜ D19 | ⬜ D20 | ⬜ D21 | ⬜ D22 | ⬜ D23 | ⬜ D24 |
| **W5** | ⬜ D25 | ⬜ D26 | ⬜ D27 | ⬜ D28 | ⬜ D29 | ⬜ D30 |

> **Legend:** 🟩 Verified Synthesis (>=300 words + Diagram + Telemetry) | 🟥 DNF (Missed Deadline / Reset) | ⬜ Pending (First Deadline: 2026-09-23 23:59 EDT)

---

#### 📊 Domain Mastery Meters
```text
Domain 1.0 Networking Concepts       [████████░░] 75%
Domain 2.0 Network Implementation    [█████░░░░░] 50%
Domain 3.0 Network Operations        [████░░░░░░] 43%
Domain 4.0 Network Security          [████░░░░░░] 44%
Domain 5.0 Network Troubleshooting   [████░░░░░░] 44%
```

---

#### ⚡ Speed Drill Benchmarks & Telemetry Records
| Drill Discipline | Personal Best | Session Average | Target Standard | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Subnetting Calculation** | `14.8s` | `21.4s` | `< 30.0s` | 🟢 Sub-30s Passed |
| **Port-to-Service Match** | `100.0%` Acc | `845ms` Latency | `< 1000ms / 100%` | 🟢 Certified |
| **Diagnostic Question Bank** | `100.0%` Acc | `5 / 5` | `> 85.0%` | 🟢 High Mastery |
| **Spaced Repetition Retention** | `2.50` Ease | `100 Cards Active` | `SM-2 Interval >= 1` | 🟢 Healthy Curve |
<!-- END_AUTOGEN_DASHBOARD -->

---

## 🏛️ Public Pledge & Rules of Engagement

1. **Daily Technical Synthesis:** Every day by 23:59 EDT, a new Markdown synthesis file must be committed to `/artifacts/day-XX-*.md`. It must contain at least **300 words**, cover byte/packet-level mechanics, include an architectural ASCII topology diagram, and detail two real-world edge-case troubleshooting scenarios.
2. **Speed Drill Quota:** Every day, at least one Subnetting Time Trial session (<30s target) and Port Speed Trial session must be completed.
3. **Automated Proctor Enforcement:** The 11:59 PM GitHub Action runs every night. If the synthesis artifact or telemetry log is missing or fails criteria, a public **`🚨 DNF ALERT`** issue is raised and the streak resets to zero.

---

## 🛠️ Architecture

```text
├── .github/workflows/
│   ├── deploy-pages.yml       # Automated GitHub Pages static host deployment
│   └── telemetry-audit.yml    # Nightly 23:59 EDT cron proctor, audit & DNF logger
├── app/                       # Zero-build vanilla ES6 client-side application
│   ├── index.html             # NOC Mission Control dashboard
│   ├── cards.html             # SuperMemo SM-2 Spaced Repetition flashcards
│   ├── drills.html            # Algorithmic subnetting & port matching trials
│   ├── css/style.css          # High-contrast terminal dark mode UI
│   └── js/                    # SM-2, subnet calculation, and telemetry modules
├── artifacts/                 # Version-controlled daily synthesis reports
├── data/                      # Cards, questions, and review state JSON
├── scripts/                   # Python audit proctor and dynamic README renderer
└── telemetry/                 # Daily logs, score records, and streak matrix state
```

---

## 🎮 Launching the Application

### Option 1: Live on GitHub Pages
Once deployed, browse to `https://<your-username>.github.io/netplus-rig/`.

### Option 2: Run Locally (Zero Build Step)
Launch any local static server from the repository root:
```bash
# Python 3
python -m http.server 8000

# Open in browser: http://localhost:8000/app/
```

---

## ⌨️ Flashcard Keyboard Controls
- `Space` or `Enter`: Flip card / reveal answer.
- `1`: Again (Failed recall / reset interval).
- `2`: Hard (Difficult recall / conservative interval).
- `3`: Good (Standard SM-2 progression).
- `4`: Easy (Bonus ease factor adjustment).
- Click **"Export Review State to Git"** to download/stage your updated `reviews.json`!
