import argparse
import csv
import datetime
import os
from pathlib import Path
import sys
import textwrap

from email_generator import generate_all_emails
from call_script_generator import generate_all_call_scripts
from onboarding_plan_generator import generate_onboarding_schedule
from training_plan_loader import load_training_plan


# ------------------------------------------------------------
# VALIDATION RULES
# ------------------------------------------------------------

REQUIRED_CANDIDATE_FIELDS = [
    "first_name",
    "last_name",
    "email",
    "role_title",
    "department",
    "team_name",
    "manager_name",
    "manager_email",
    "start_date",
    "work_location",
    "working_pattern",
    "salary_details",
    "contract_type",
    "probation_length",
    "security_clearance_required",
    "equipment_needed",
    "remote_access_required",
    "recruitment_portal_link"
]

REQUIRED_TRAINING_FIELDS = [
    "day_offset",
    "time",
    "title",
    "owner"
]


# ------------------------------------------------------------
# CSV VALIDATION
# ------------------------------------------------------------

def validate_candidate_row(row):
    errors = []

    # Check required fields exist and are not blank
    for field in REQUIRED_CANDIDATE_FIELDS:
        if field not in row or row[field].strip() == "":
            errors.append(f"Missing required field: {field}")

    # Validate date format
    if "start_date" in row and row["start_date"].strip():
        try:
            datetime.datetime.strptime(row["start_date"], "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid date format for start_date (expected YYYY-MM-DD)")

    # Validate URL
    if "recruitment_portal_link" in row:
        link = row["recruitment_portal_link"].strip()
        if not (link.startswith("http://") or link.startswith("https://")):
            errors.append("Invalid recruitment_portal_link (must start with http:// or https://)")

    # Validate boolean-like fields
    for field in ["remote_access_required", "security_clearance_required"]:
        if field in row:
            val = row[field].strip().lower()
            if val not in ["yes", "no", "true", "false"]:
                errors.append(f"Invalid value for {field} (expected Yes/No/True/False)")

    # Validate equipment list formatting
    if "equipment_needed" in row:
        if "," in row["equipment_needed"]:
            errors.append("equipment_needed should use semicolons (;) not commas")

    return errors


def validate_training_plan(path):
    errors = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Check required columns
        for field in REQUIRED_TRAINING_FIELDS:
            if field not in reader.fieldnames:
                errors.append(f"Training plan missing required column: {field}")

        # Validate rows
        for i, row in enumerate(reader, start=2):
            # Blank row check
            if not any(row.values()):
                errors.append(f"Row {i}: Empty or malformed row")
                continue

            # day_offset
            try:
                offset = int(row["day_offset"])
                if offset < 0:
                    errors.append(f"Row {i}: day_offset must be non-negative")
            except ValueError:
                errors.append(f"Row {i}: day_offset must be an integer")

            # time format
            try:
                datetime.datetime.strptime(row["time"], "%H:%M")
            except ValueError:
                errors.append(f"Row {i}: Invalid time format '{row['time']}' (expected HH:MM)")

            # title / owner
            if not row["title"].strip():
                errors.append(f"Row {i}: Missing required field: title")
            if not row["owner"].strip():
                errors.append(f"Row {i}: Missing required field: owner")

    return errors


# ------------------------------------------------------------
# OUTPUT HELPERS
# ------------------------------------------------------------

def timestamp():
    return datetime.date.today().strftime("%Y-%m-%d")


def write_output_file(base_path, filename, content):
    base_path.mkdir(parents=True, exist_ok=True)
    file_path = base_path / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def print_section(title, content):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(content)


# ------------------------------------------------------------
# MAIN LOGIC
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="HR Automation Toolkit — Generate onboarding packs, emails, and scripts."
    )

    parser.add_argument("--candidate", required=True, help="Path to candidate CSV file")
    parser.add_argument("--training-plan", help="Path to training plan CSV file")

    # Combinable modes
    parser.add_argument("-e", "--emails-only", action="store_true")
    parser.add_argument("-c", "--call-scripts-only", action="store_true")
    parser.add_argument("-d", "--countdown-only", action="store_true")
    parser.add_argument("-o", "--onboarding-only", action="store_true")
    parser.add_argument("-f", "--offer-only", action="store_true")
    parser.add_argument("-a", "--everything", action="store_true")

    args = parser.parse_args()

    # Load candidate CSV
    with open(args.candidate, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("❌ Candidate CSV is empty.")
        sys.exit(1)

    candidate = rows[0]  # First row only

    # Validate candidate CSV
    candidate_errors = validate_candidate_row(candidate)

    # Validate training plan if needed
    training_errors = []
    onboarding_requested = args.onboarding_only or args.everything

    if onboarding_requested:
        if not args.training_plan:
            print("❌ Onboarding requested but no training plan CSV provided.")
            sys.exit(1)
        training_errors = validate_training_plan(args.training_plan)

    # Collect all errors
    all_errors = candidate_errors + training_errors

    if all_errors:
        print("\n❌ Validation failed\n")
        print("The following issues were found:\n")
        for err in all_errors:
            print(f"- {err}")
        print("\nPlease correct these issues and try again.")
        sys.exit(1)

    # Determine which outputs to generate
    generate_all = args.everything

    generate_emails = generate_all or args.emails_only
    generate_call_scripts = generate_all or args.call_scripts_only
    generate_countdown = generate_all or args.countdown_only
    generate_onboarding = generate_all or args.onboarding_only
    generate_offer = generate_all or args.offer_only

    # Prepare output folder
    candidate_name = f"{candidate['first_name']}_{candidate['last_name']}".replace(" ", "_")
    output_dir = Path("output") / candidate_name
    today = timestamp()

    # ------------------------------------------------------------
    # EMAILS
    # ------------------------------------------------------------
    if generate_emails:
        emails = generate_all_emails(candidate)
        for name, content in emails.items():
            filename = f"{today}_{candidate_name}_{name}.md"
            write_output_file(output_dir, filename, content)
            print_section(f"EMAIL: {name}", content)

    # ------------------------------------------------------------
    # CALL SCRIPTS
    # ------------------------------------------------------------
    if generate_call_scripts:
        scripts = generate_all_call_scripts(candidate)
        for name, content in scripts.items():
            filename = f"{today}_{candidate_name}_{name}.md"
            write_output_file(output_dir, filename, content)
            print_section(f"CALL SCRIPT: {name}", content)

    # ------------------------------------------------------------
    # OFFER EMAIL + CALL SCRIPT
    # ------------------------------------------------------------
    if generate_offer:
        offer_emails = generate_all_emails(candidate, offer_only=True)
        offer_scripts = generate_all_call_scripts(candidate, offer_only=True)

        for name, content in offer_emails.items():
            filename = f"{today}_{candidate_name}_{name}.md"
            write_output_file(output_dir, filename, content)
            print_section(f"OFFER EMAIL: {name}", content)

        for name, content in offer_scripts.items():
            filename = f"{today}_{candidate_name}_{name}.md"
            write_output_file(output_dir, filename, content)
            print_section(f"OFFER CALL SCRIPT: {name}", content)

    # ------------------------------------------------------------
    # COUNTDOWN EMAILS
    # ------------------------------------------------------------
    if generate_countdown:
        countdowns = generate_all_emails(candidate, countdown_only=True)
        for name, content in countdowns.items():
            filename = f"{today}_{candidate_name}_{name}.md"
            write_output_file(output_dir, filename, content)
            print_section(f"COUNTDOWN EMAIL: {name}", content)

    # ------------------------------------------------------------
    # ONBOARDING SCHEDULE
    # ------------------------------------------------------------
    if generate_onboarding:
        training_plan = load_training_plan(Path(args.training_plan))
        schedule_md = generate_onboarding_schedule(candidate, training_plan)

        filename = f"{today}_{candidate_name}_onboarding_schedule.md"
        write_output_file(output_dir, filename, schedule_md)
        print_section("ONBOARDING SCHEDULE", schedule_md)


if __name__ == "__main__":
    main()
