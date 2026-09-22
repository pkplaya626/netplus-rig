#!/usr/bin/env python3
"""
CompTIA Network+ (N10-009) Sprint Audit Proctor.
Validates daily technical synthesis artifacts (>=300 words, headers, ASCII topology diagram)
and verifies daily telemetry entries in progress.json.
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def count_words(text: str) -> int:
    """Counts words in a markdown string, excluding code block formatting fences."""
    lines = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        lines.append(line)
    clean_text = "\n".join(lines)
    words = re.findall(r"\b[\w'-]+\b", clean_text)
    return len(words)


def find_artifact_for_day(repo_root: Path, day: int) -> Path | None:
    """Locates the artifact markdown file matching day-XX-*.md or day-X-*.md."""
    day_str_2 = f"{day:02d}"
    day_str_1 = f"{day}"
    patterns = [
        f"artifacts/day-{day_str_2}-*.md",
        f"artifacts/day-{day_str_1}-*.md",
        f"artifacts/day_{day_str_2}_*.md",
        f"artifacts/day_{day_str_1}_*.md",
        f"artifacts/day-{day_str_2}.md",
        f"artifacts/day-{day_str_1}.md",
    ]
    for pattern in patterns:
        matches = list(repo_root.glob(pattern))
        if matches:
            return matches[0]
    return None


def validate_artifact(file_path: Path) -> tuple[bool, list[str]]:
    """Validates artifact for word count, required headers, and ASCII diagrams."""
    errors = []
    if not file_path.exists():
        return False, [f"Artifact file not found: {file_path}"]

    content = file_path.read_text(encoding="utf-8")
    words = count_words(content)

    if words < 300:
        errors.append(
            f"Artifact word count is {words}, which is below the mandatory 300-word threshold."
        )

    # Check required section headers
    required_sections = [
        (r"##\s*1\.\s*Technical Mechanics", "1. Technical Mechanics (Deep Breakdown)"),
        (r"##\s*2\.\s*Architectural ASCII", "2. Architectural ASCII / Topology Diagram"),
        (r"##\s*3\.\s*Edge Cases", "3. Edge Cases & Troubleshooting Scenarios"),
    ]

    for pattern, name in required_sections:
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Missing required section header: '{name}'")

    # Check ASCII diagram presence
    has_code_block = re.search(r"```(text|ascii|)?\s*\n(.*?\+.*?|.*?\|.*?|.*?-->.*?)\n```", content, re.DOTALL)
    if not has_code_block:
        # Fallback check for any code block with box drawing or topology characters
        blocks = re.findall(r"```.*?\n(.*?)```", content, re.DOTALL)
        found_ascii = False
        for b in blocks:
            if any(char in b for char in ["+", "|", "---", "-->", "===", "\\", "/"]):
                found_ascii = True
                break
        if not found_ascii:
            errors.append("Missing required architectural ASCII / topology diagram inside a fenced code block.")

    return len(errors) == 0, errors


def validate_telemetry(repo_root: Path, day: int) -> tuple[bool, list[str]]:
    """Verifies that progress.json has a valid record for the given day with activity."""
    errors = []
    progress_file = repo_root / "telemetry" / "progress.json"
    if not progress_file.exists():
        return False, ["telemetry/progress.json does not exist."]

    try:
        with open(progress_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Failed to parse telemetry/progress.json: {e}"]

    daily_logs = data.get("dailyLogs", {})
    day_key = str(day)

    if day_key not in daily_logs:
        errors.append(f"No daily log entry found in telemetry/progress.json for Day {day}.")
        return False, errors

    log_entry = daily_logs[day_key]
    cards = log_entry.get("cardsReviewed", 0)
    questions = log_entry.get("questionsCleared", 0)
    subnet_attempts = log_entry.get("subnetDrill", {}).get("attempts", 0)
    port_attempts = log_entry.get("portDrill", {}).get("attempts", 0)

    total_activity = cards + questions + subnet_attempts + port_attempts
    if total_activity <= 0:
        errors.append(
            f"Day {day} log exists in telemetry/progress.json, but has 0 cards, questions, or drill attempts logged."
        )

    return len(errors) == 0, errors


def update_streak(repo_root: Path, day: int, is_green: bool):
    """Updates telemetry/streak.json with the day outcome (GREEN or RED)."""
    streak_file = repo_root / "telemetry" / "streak.json"
    streak_data = {
        "currentStreak": 0,
        "longestStreak": 0,
        "lastEvaluatedDay": day,
        "lastEvaluatedTimestamp": datetime.now(timezone.utc).isoformat(),
        "days": {str(d): "PENDING" for d in range(1, 31)}
    }

    if streak_file.exists():
        try:
            with open(streak_file, "r", encoding="utf-8") as f:
                streak_data = json.load(f)
        except Exception:
            pass

    day_key = str(day)
    days_map = streak_data.setdefault("days", {})

    if is_green:
        days_map[day_key] = "GREEN"
        # Recalculate streak
        streak = 0
        max_streak = streak_data.get("longestStreak", 0)
        for d in range(1, 31):
            status = days_map.get(str(d), "PENDING")
            if status == "GREEN":
                streak += 1
                if streak > max_streak:
                    max_streak = streak
            elif status == "RED":
                streak = 0
            else:
                break
        streak_data["currentStreak"] = streak
        streak_data["longestStreak"] = max_streak
    else:
        days_map[day_key] = "RED"
        streak_data["currentStreak"] = 0

    streak_data["lastEvaluatedDay"] = day
    streak_data["lastEvaluatedTimestamp"] = datetime.now(timezone.utc).isoformat()

    streak_file.parent.mkdir(parents=True, exist_ok=True)
    with open(streak_file, "w", encoding="utf-8") as f:
        json.dump(streak_data, f, indent=2)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="CompTIA Network+ Sprint Audit Proctor")
    parser.add_argument("--day", type=int, default=None, help="Sprint day to audit (1-30)")
    parser.add_argument("--root", type=str, default=".", help="Root repository directory")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()

    # Determine day to audit
    day = args.day
    if day is None:
        streak_file = repo_root / "telemetry" / "streak.json"
        if streak_file.exists():
            try:
                with open(streak_file, "r", encoding="utf-8") as f:
                    sdata = json.load(f)
                    day = sdata.get("lastEvaluatedDay", 1)
            except Exception:
                day = 1
        else:
            day = 1

    print("=" * 60)
    print(f"  [NETPLUS RIG] DAILY AUDIT PROCTOR: DAY {day:02d} / 30")
    print("=" * 60)

    all_errors = []

    # 1. Check synthesis artifact
    artifact_file = find_artifact_for_day(repo_root, day)
    if not artifact_file:
        all_errors.append(f"Missing synthesis markdown file for Day {day:02d} (expected artifacts/day-{day:02d}-*.md)")
    else:
        print(f"✓ Found synthesis artifact: {artifact_file.name}")
        art_valid, art_errors = validate_artifact(artifact_file)
        if art_valid:
            print(f"✓ Synthesis artifact meets word count (>=300), structure, and ASCII diagram specs.")
        else:
            all_errors.extend(art_errors)

    # 2. Check telemetry
    tel_valid, tel_errors = validate_telemetry(repo_root, day)
    if tel_valid:
        print(f"✓ Telemetry record confirmed in telemetry/progress.json for Day {day:02d}.")
    else:
        all_errors.extend(tel_errors)

    # Output audit failure details if any
    summary_file = repo_root / "telemetry" / "last_audit_result.json"
    summary_file.parent.mkdir(parents=True, exist_ok=True)

    if all_errors:
        print("\n❌ AUDIT FAILED (DNF):")
        for err in all_errors:
            print(f"  - {err}")
        update_streak(repo_root, day, is_green=False)
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump({
                "day": day,
                "passed": False,
                "status": "RED",
                "errors": all_errors,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }, f, indent=2)
        sys.exit(1)
    else:
        print("\n✅ AUDIT PASSED: Day marked GREEN.")
        update_streak(repo_root, day, is_green=True)
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump({
                "day": day,
                "passed": True,
                "status": "GREEN",
                "errors": [],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }, f, indent=2)
        sys.exit(0)


if __name__ == "__main__":
    main()
