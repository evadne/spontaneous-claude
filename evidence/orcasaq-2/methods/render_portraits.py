"""Validate and preview visible SVG output without changing the original response."""

import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
portrait_dirs = sorted((root / "controls").glob("portrait-*")) + sorted(
    (root / "base-control").glob("portrait-*")
)
for directory in portrait_dirs:
    response_file = directory / "response.json"
    if not response_file.exists():
        continue
    response = json.loads(response_file.read_text())
    content = response["choices"][0]["message"].get("content") or ""
    start = content.find("<svg")
    end = content.rfind("</svg>")
    if start < 0 or end < 0:
        print(directory.name, "no complete visible SVG")
        continue
    svg = content[start : end + len("</svg>")]
    try:
        root_element = ET.fromstring(svg)
        assert root_element.tag.endswith("svg")
        (directory / "portrait.svg").write_text(svg)
        rendered = subprocess.run(
            ["rsvg-convert", "-o", str(directory / "portrait.png"), str(directory / "portrait.svg")],
            text=True, capture_output=True, check=False,
        )
        (directory / "render.log").write_text(rendered.stdout + rendered.stderr)
        print(directory.name, "SVG parsed", "PNG rendered" if rendered.returncode == 0 else "PNG failed")
    except (ET.ParseError, AssertionError) as error:
        (directory / "render.log").write_text(str(error))
        print(directory.name, "invalid SVG", error)
