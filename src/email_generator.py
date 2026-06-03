import os
from pathlib import Path


TEMPLATE_DIR = Path("templates/emails")


def load_template(name):
    """Load a Markdown email template by filename."""
    path = TEMPLATE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Email template not found: {path}")
    return path.read_text(encoding="utf-8")


def render_template(template, candidate):
    """Replace {{placeholders}} in templates with candidate metadata."""
    text = template
    for key, value in candidate.items():
        placeholder = f"{{{{{key}}}}}"
        text = text.replace(placeholder, value)
    return text


def generate_rejection_emails(candidate):
    """Generate all rejection emails."""
    templates = {
        "rejection_not_shortlisted": "rejection_not_shortlisted.md",
        "rejection_after_screening": "rejection_after_screening.md",
        "rejection_after_interview": "rejection_after_interview.md",
    }

    output = {}
    for key, filename in templates.items():
        template = load_template(filename)
        output[key] = render_template(template, candidate)

    return output


def generate_offer_email(candidate):
    """Generate the offer email."""
    template = load_template("offer_email.md")
    return {"offer_email": render_template(template, candidate)}


def generate_countdown_emails(candidate):
    """Generate T‑14, T‑7, T‑1 countdown emails."""
    templates = {
        "countdown_t_minus_14": "countdown_t_minus_14.md",
        "countdown_t_minus_7": "countdown_t_minus_7.md",
        "countdown_t_minus_1": "countdown_t_minus_1.md",
    }

    output = {}
    for key, filename in templates.items():
        template = load_template(filename)
        output[key] = render_template(template, candidate)

    return output


def generate_all_emails(candidate, offer_only=False, countdown_only=False):
    """
    Generate all email types depending on mode.
    Called by main.py.
    """
    if offer_only:
        return generate_offer_email(candidate)

    if countdown_only:
        return generate_countdown_emails(candidate)

    # Default: all rejection + offer + countdown
    emails = {}
    emails.update(generate_rejection_emails(candidate))
    emails.update(generate_offer_email(candidate))
    emails.update(generate_countdown_emails(candidate))
    return emails
