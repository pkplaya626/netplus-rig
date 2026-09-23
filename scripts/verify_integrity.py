#!/usr/bin/env python3
"""
Verification test script for CompTIA Network+ Training Rig repository integrity.
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_root = Path(__file__).resolve().parent.parent

print("Running Repository Integrity Checks...")

# 1. Cards
cards_path = repo_root / "data" / "cards.json"
assert cards_path.exists(), "data/cards.json missing"
with open(cards_path, "r", encoding="utf-8") as f:
    cards = json.load(f)
print(f"[OK] data/cards.json: {len(cards)} cards loaded (Requirement: 100+)")
assert len(cards) >= 100, f"Expected at least 100 cards, got {len(cards)}"

# 2. Questions
q_path = repo_root / "data" / "questions.json"
assert q_path.exists(), "data/questions.json missing"
with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)
print(f"[OK] data/questions.json: {len(questions)} questions loaded (Requirement: 40+)")
assert len(questions) >= 40, f"Expected at least 40 questions, got {len(questions)}"

# 3. Reviews
r_path = repo_root / "data" / "reviews.json"
assert r_path.exists(), "data/reviews.json missing"
with open(r_path, "r", encoding="utf-8") as f:
    reviews = json.load(f)
print(f"[OK] data/reviews.json: {len(reviews.get('cards', {}))} card schedules loaded")

# 4. Telemetry Progress & Streak
p_path = repo_root / "telemetry" / "progress.json"
s_path = repo_root / "telemetry" / "streak.json"
assert p_path.exists(), "telemetry/progress.json missing"
assert s_path.exists(), "telemetry/streak.json missing"
with open(p_path, "r", encoding="utf-8") as f:
    prog = json.load(f)
with open(s_path, "r", encoding="utf-8") as f:
    streak = json.load(f)
print(f"[OK] telemetry/progress.json & streak.json: active streak {streak.get('currentStreak')}")

# 5. Day 1 Artifact & Systemic Analysis Doc
art_path = repo_root / "artifacts" / "day-01-osi-and-packet-flow.md"
assert art_path.exists(), "day-01 artifact missing"
with open(art_path, "r", encoding="utf-8") as f:
    art_text = f.read()
import re
words = len(re.findall(r"\b[\w'-]+\b", art_text))
print(f"[OK] artifacts/day-01-osi-and-packet-flow.md: {words} words (Requirement: >= 300)")
assert words >= 300, f"Expected at least 300 words, got {words}"

doc_path = repo_root / "docs" / "systemic-analysis.md"
assert doc_path.exists(), "docs/systemic-analysis.md missing"
print("[OK] docs/systemic-analysis.md: Systemic analysis architecture doc present")

# 6. Web App Files
app_files = [
    "app/index.html",
    "app/cards.html",
    "app/drills.html",
    "app/reference.html",
    "app/css/style.css",
    "app/js/sm2.js",
    "app/js/cards.js",
    "app/js/subnet-drill.js",
    "app/js/port-drill.js",
    "app/js/telemetry.js"
]
for af in app_files:
    p = repo_root / af
    assert p.exists(), f"Missing web asset: {af}"
print(f"[OK] Web application: all {len(app_files)} HTML, CSS, and JS components present")

# 7. GitHub Actions Workflows
wf_files = [
    ".github/workflows/deploy-pages.yml",
    ".github/workflows/telemetry-audit.yml"
]
for wf in wf_files:
    p = repo_root / wf
    assert p.exists(), f"Missing workflow: {wf}"
print(f"[OK] GitHub Actions: all {len(wf_files)} workflows present")

print("\nALL REPOSITORY INTEGRITY CHECKS PASSED SUCCESSFULLY!")
