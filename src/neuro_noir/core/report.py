from typing import Optional


def md_report(
    title: str,
    what_went_wrong: str,
    likely_causes: list[str],
    how_to_fix: list[str],
    details: Optional[list[str]] = None,
) -> str:
    """Build a beginner-friendly Markdown report with 3 parts."""
    lines: list[str] = []
    lines.append(f"### {title}\n")
    lines.append("**1) What went wrong**\n")
    lines.append(f"- {what_went_wrong}\n")
    lines.append("**2) What could have caused that**\n")
    for c in likely_causes:
        lines.append(f"- {c}")
    lines.append("\n**3) How to fix it**\n")
    for f in how_to_fix:
        lines.append(f"- {f}")

    if details:
        lines.append("\n---\n**Details (for debugging)**")
        for d in details:
            lines.append(f"- {d}")

    return "\n".join(lines)