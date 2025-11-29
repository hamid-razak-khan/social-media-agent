from __future__ import annotations

from datetime import datetime
from typing import Dict


def _slugify(value: str) -> str:
    """Convert text to a simple filename-safe slug."""
    if not value:
        return ""
    cleaned = value.strip().lower().replace("/", "-")
    return "-".join(part for part in cleaned.split() if part)


def build_filename(business_type: str, platform: str, content_type: str) -> str:
    """Build a descriptive filename for downloaded content."""
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    parts = [_slugify(business_type), _slugify(platform), _slugify(content_type)]
    base = "-".join([p for p in parts if p]) or "social-content"
    return f"{base}-{timestamp}.txt"


def wrap_content_for_download(content: str, meta: Dict[str, str]) -> str:
    """Wrap generated content with simple metadata for plain-text download."""
    lines = [
        "Social Media Content Generator Output",
        "----------------------------------",
    ]

    for key, value in meta.items():
        if value:
            lines.append(f"{key}: {value}")

    lines.extend([
        "",
        "Generated Content",
        "-----------------",
        "",
        content.strip(),
        "",
    ])

    return "\n".join(lines)
