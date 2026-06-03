from pathlib import Path

TEMPLATE_DIR = Path("templates/call_scripts")


def load_template(name):
    """Load a Markdown call script template by filename."""
    path = TEMPLATE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Call script template not found: {path}")
    return path.read_text(encoding="utf-8")


def render_template(template, candidate):
    """Replace {{placeholders}} in templates with candidate metadata."""
    text = template
    for key, value in candidate.items():
        placeholder = f"{{{{{key}}}}}"
        text = text.replace(placeholder, value)
    return text


def generate_rejection_call_scripts(candidate):
    """Generate screening and interview rejection call scripts."""
    templates = {
        "rejection_screening_call": "rejection_screening_call.md",
        "rejection_interview_call": "rejection_interview_call.md",
    }

    output = {}
    for key, filename in templates.items():
        template = load_template(filename)
        output[key] = render_template(template, candidate)

    return output


def generate_offer_call_script(candidate):
    """Generate the offer call script."""
    template = load_template("offer_call_script.md")
    return {"offer_call_script": render_template(template, candidate)}


def generate_all_call_scripts(candidate, offer_only=False):
    """
    Generate all call scripts depending on mode.
    Called by main.py.
    """
    if offer_only:
        return generate_offer_call_script(candidate)

    scripts = {}
    scripts.update(generate_rejection_call_scripts(candidate))
    scripts.update(generate_offer_call_script(candidate))
    return scripts
