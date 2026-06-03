from pathlib import Path
import yaml
from datetime import datetime, timedelta


CORE_ONBOARDING_PATH = Path("templates/onboarding/core_onboarding.yaml")


def load_core_onboarding_tasks():
    """Load the core HR onboarding tasks from YAML."""
    if not CORE_ONBOARDING_PATH.exists():
        raise FileNotFoundError(f"Core onboarding file not found: {CORE_ONBOARDING_PATH}")

    with open(CORE_ONBOARDING_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def format_date(start_date_str, day_offset):
    """Return a date string for the onboarding schedule."""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    target_date = start_date + timedelta(days=day_offset)
    return target_date.strftime("%Y-%m-%d")


def generate_markdown_section(title, items):
    """Format a section of the onboarding plan as Markdown."""
    md = [f"## {title}\n"]
    for item in items:
        md.append(f"- **{item['time']}** — {item['title']} _(Owner: {item['owner']})_")
    md.append("")  # blank line
    return "\n".join(md)


def merge_tasks(core_tasks, training_tasks, start_date):
    """
    Merge core HR tasks and role-specific training tasks into a single
    chronological structure grouped by day.
    """
    schedule = {}

    # Add core tasks
    for task in core_tasks:
        day = task["day_offset"]
        schedule.setdefault(day, [])
        schedule[day].append({
            "time": task["time"],
            "title": task["title"],
            "owner": task["owner"]
        })

    # Add training tasks
    for task in training_tasks:
        day = int(task["day_offset"])
        schedule.setdefault(day, [])
        schedule[day].append({
            "time": task["time"],
            "title": task["title"],
            "owner": task["owner"]
        })

    # Sort tasks within each day by time
    for day in schedule:
        schedule[day] = sorted(schedule[day], key=lambda x: x["time"])

    return schedule


def generate_onboarding_schedule(candidate, training_plan):
    """
    Generate the full onboarding schedule as Markdown.
    """
    core_tasks = load_core_onboarding_tasks()
    start_date = candidate["start_date"]

    merged = merge_tasks(core_tasks, training_plan, start_date)

    md = []
    md.append(f"# Onboarding Schedule for {candidate['first_name']} {candidate['last_name']}")
    md.append(f"**Role:** {candidate['role_title']}")
    md.append(f"**Start Date:** {candidate['start_date']}")
    md.append("")

    # Build day-by-day sections
    for day_offset in sorted(merged.keys()):
        date_str = format_date(start_date, day_offset)
        md.append(f"---\n")
        md.append(f"# Day {day_offset} — {date_str}\n")
        md.append(generate_markdown_section("Planned Activities", merged[day_offset]))

    return "\n".join(md)
