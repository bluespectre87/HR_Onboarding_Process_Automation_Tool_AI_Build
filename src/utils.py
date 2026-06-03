from datetime import datetime
from pathlib import Path


def ensure_directory(path: Path):
    """
    Create a directory if it doesn't already exist.
    """
    path.mkdir(parents=True, exist_ok=True)


def iso_today():
    """
    Return today's date in ISO format (YYYY-MM-DD).
    """
    return datetime.today().strftime("%Y-%m-%d")


def replace_placeholders(text: str, data: dict) -> str:
    """
    Replace {{placeholders}} in a text block using a dictionary of values.
    """
    for key, value in data.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def print_header(title: str):
    """
    Print a clean, readable section header to the terminal.
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
