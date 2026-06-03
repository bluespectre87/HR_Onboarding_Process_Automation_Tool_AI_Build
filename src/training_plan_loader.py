import csv
from pathlib import Path


def load_training_plan(path: Path):
    """
    Load the role-specific training plan CSV and return a list of dicts.
    Assumes validation has already been performed in main.py.
    """
    tasks = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Skip empty rows
            if not any(row.values()):
                continue

            tasks.append({
                "day_offset": row["day_offset"].strip(),
                "time": row["time"].strip(),
                "title": row["title"].strip(),
                "owner": row["owner"].strip(),
            })

    return tasks
