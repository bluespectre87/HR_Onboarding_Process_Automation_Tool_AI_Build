# HR Onboarding & Candidate Communication Automation Tool

This project is a fully modular, CLI‑based automation tool designed to streamline HR processes including:

- Candidate communication (emails + call scripts)
- Offer communication
- Countdown‑to‑start emails
- Onboarding plan generation
- Integration of role‑specific training plans
- Clean Markdown output for GitHub, ATS, or internal documentation

The tool is built for clarity, maintainability, and extensibility — making it easy to adapt for different teams, roles, and organisations.

**Please see 'USAGE.md' for a step by step guide to use this tool**

---

## 🚀 Features

### **1. Candidate Communication Generator**
Generates:
- Rejection emails (3 variants)
- Rejection call scripts (2 variants)
- Offer email
- Offer call script

All templates are:
- Markdown‑formatted  
- Placeholder‑driven  
- Written in a warm, human, professional tone  

---

### **2. Onboarding Pack Generator**
Creates a complete onboarding schedule by merging:
- Core HR onboarding tasks (YAML)
- Role‑specific training plan (CSV)
- Candidate metadata (JSON)

Outputs a clean, chronological Markdown onboarding plan.

---

### **3. Countdown Emails**
Automatically generates:
- T‑14 email  
- T‑7 email  
- T‑1 email  

Designed to reduce first‑day anxiety and support a smooth transition.

## 🧩 Customisation

You can customise:

- Email tone  
- Call scripts  
- Onboarding tasks  
- Training plans  
- Company configuration  

All templates are fully editable and placeholder‑driven.

---

## 📂 Project Structure

.
├── src/
│   ├── main.py
│   ├── email_generator.py
│   ├── call_script_generator.py
│   ├── onboarding_plan_generator.py
│   ├── training_plan_loader.py
│   └── utils.py
│
├── templates/
│   ├── emails/
│   │   ├── rejection_not_shortlisted.md
│   │   ├── rejection_after_screening.md
│   │   ├── rejection_after_interview.md
│   │   ├── offer_email.md
│   │   ├── countdown_t_minus_14.md
│   │   ├── countdown_t_minus_7.md
│   │   └── countdown_t_minus_1.md
│   │
│   ├── call_scripts/
│   │   ├── rejection_screening_call.md
│   │   ├── rejection_interview_call.md
│   │   └── offer_call_script.md
│   │
│   └── onboarding/
│       └── core_onboarding.yaml
│
├── config/
│   ├── company_config.yaml
│   └── training_plan_example.csv
│
├── output/
│   └── (auto‑generated files)
│
├── sample_candidate.json
└── README.md