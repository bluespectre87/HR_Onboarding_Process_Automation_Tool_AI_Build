📘 USAGE GUIDE — How to Use the HR Automation Tool
A simple, visual, step‑by‑step guide with examples

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

🧭 Step‑by‑Step Guide
🟦 STEP 1 — Clone or download the repository
**If using Git:**
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
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
company:
  name: "Example Organisation"
  timezone: "Europe/London"
defaults:
  working_pattern: "Full-time"
teams:
  People & Culture:
    manager_name: "Emily Carter"


🟨 STEP 3 — Prepare a training plan CSV (per role)
📍 Location: config/training_plan_example.csv
This file defines role‑specific training tasks.

Example:
day_offset,time,title,owner
1,15:00,Introduction to team tools,Manager
2,09:00,Shadowing: core workflow,Manager
3,10:00,Role-specific training module 1,Manager

✏️ When you need to edit this file:
- When a new role is created
- When training content changes
- When you want to add/remove tasks
- You can create as many CSVs as you want — one per role.

🟧 STEP 4 — Create a candidate JSON file (per candidate)
📍 Location: sample_candidate.json
**Example:**
{
  "first_name": "Alex",
  "role_title": "People Operations Specialist",
  "team_name": "People & Culture",
  "manager_name": "Emily Carter",
  "start_date": "2026-07-01"
}
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
📍 Location:templates/
templates/
You can edit:
- Email templates
- Call scripts
- Onboarding YAML

✏️ When you need to edit templates:
- Tone of voice changes
- New process steps
- New email variants
- New onboarding tasks

Templates use placeholders like:
{{first_name}}
{{role_title}}
{{start_date}}
{{manager_name}}
These are automatically replaced by the tool.

🎨 Visual Summary
          ┌──────────────────────────────┐
          │   1. Clone the repository    │
          └───────────────┬──────────────┘
                          ▼
          ┌──────────────────────────────┐
          │ 2. Update company_config.yaml│
          └───────────────┬──────────────┘
                          ▼
          ┌──────────────────────────────┐
          │ 3. Create training CSV       │
          └───────────────┬──────────────┘
                          ▼
          ┌──────────────────────────────┐
          │ 4. Create candidate JSON     │
          └───────────────┬──────────────┘
                          ▼
          ┌──────────────────────────────┐
          │ 5. Run CLI command           │
          └───────────────┬──────────────┘
                          ▼
          ┌──────────────────────────────┐
          │ 6. Review output/ folder     │
          └───────────────┬──────────────┘
                          ▼
          ┌──────────────────────────────┐
          │ 7. Edit templates if needed  │
          └──────────────────────────────┘


🧩 Key CLI Commands (Quick Reference)
Generate onboarding + emails + scripts:
python src/main.py --candidate sample_candidate.json --training config/training_plan_example.csv

Use a different training plan:
python src/main.py --candidate candidate.json --training config/tech_training.csv

Use a different candidate file:
python src/main.py --candidate candidates/jordan.json --training config/training_plan_example.csv
