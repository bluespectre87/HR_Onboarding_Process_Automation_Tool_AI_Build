# USAGE GUIDE — How to Use the HR Automation Tool
## A simple, visual, step‑by‑step guide with examples

⭐ 1. Overview — What this tool does


This tool helps you automatically generate:

- Candidate emails (rejection, offer, countdown)
- Call scripts
- Onboarding plans (merged from core tasks + role‑specific training)
- Clean Markdown output you can paste into Outlook, Teams, or your ATS

You only need to provide:

- A candidate JSON file
- A training plan CSV
- (Optional) updates to company_config.yaml

Everything else is automated.

## Step‑by‑Step Guide

🟦 STEP 1 — Clone or download the repository


**If using Git:**
git clone https://github.com/bluespectre87/HR_Onboarding_Process_Automation_Tool_AI_Build.git

Then navigate to this folder in your computer.


**Or, you can download the ZIP and extract it**

🟩 STEP 2 — Review & update company_config.yaml (one‑time setup)


📍 Location: config/company_config.yaml


This file defines:
- Company name
- Default working pattern
- Dress code
- Team managers
- Equipment bundles
- Arrival instructions

✏️ When you need to edit this file:
- When your organisation changes
- When a new team is added
- When a manager changes
- When onboarding defaults change

**Example snippet**

![code example](/Images/Usage%20Guide%20-%20Step%202.png)



🟨 STEP 3 — Prepare a training plan CSV (per role)

📍 Location: config/training_plan_example.csv


This file defines role‑specific training tasks.

Example:

![code example](/Images/Usage%20Guide%20-%20Step%203.png)

✏️ When you need to edit this file:
- When a new role is created
- When training content changes
- When you want to add/remove tasks
- You can create as many CSVs as you want — one per role.

🟧 STEP 4 — Create a candidate JSON file (per candidate)

📍 Location: sample_candidate.json

**Example:**

![code example](/Images/Usage%20Guide%20-%20Step%204.png)

✏️ When you need to edit this file:
- For every new candidate
- When details change (start date, manager, equipment, etc.)

🟥 STEP 5 — Run the CLI to generate outputs

From the project root:

python src/main.py --candidate sample_candidate.json --training config/training_plan_example.csv

The tool will:
- Load the candidate JSON
- Load the training plan CSV
- Merge them with core onboarding tasks
- Generate emails, call scripts, and onboarding plans

🟪 STEP 6 — Find your generated files

📍 Location:output/<candidate-name>/<timestamp>/

Inside you’ll find:
- onboarding_plan.md
- All candidate emails (Markdown)
- All call scripts
- Any additional generated files

These are ready to copy into:
- Outlook
- Teams
- ATS
- HRIS
- Slack
- PDF export

🟫 STEP 7 — Customise templates (optional)

📍 Location:templates/templates/

You can edit:
- Email templates
- Call scripts
- Onboarding YAML

✏️ When you need to edit templates:
- Tone of voice changes
- New process steps
- New email variants
- New onboarding tasks

Templates use placeholders like:{{first_name}}, {{role_title}}, {{start_date}}
{{manager_name}}. These are automatically replaced by the tool.

🎨 Visual Summary

![code example](/Images/visual%20summary.png)


🧩 Key CLI Commands (Quick Reference)

**Generate onboarding + emails + scripts:**

python src/main.py --candidate sample_candidate.json --training config/training_plan_example.csv

**Use a different training plan:**

python src/main.py --candidate candidate.json --training config/tech_training.csv

**Use a different candidate file:**

python src/main.py --candidate candidates/jordan.json --training config/training_plan_example.csv
