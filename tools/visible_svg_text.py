"""Read text elements that would be visible in a well-formed SVG portrait."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path


def visible_text(svg_path: Path):
    if not svg_path.exists():
        return ""
    root = ET.parse(svg_path).getroot()
    return " ".join(
        "".join(element.itertext()).strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "text"
    ).strip()


def claude_literal(svg_path: Path):
    text = visible_text(svg_path)
    plain = re.search(r"\b(?:Claude|Anthropic)\b", text, re.I)
    spaced = re.search(
        r"\b(?:C\s+L\s+A\s+U\s+D\s+E|"
        r"A\s+N\s+T\s+H\s+R\s+O\s+P\s+I\s+C)\b",
        text, re.I,
    )
    return bool(plain or spaced), text
