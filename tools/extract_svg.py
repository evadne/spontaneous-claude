"""Original portrait-farm SVG extraction and recorded rendering repairs."""

import html.entities
import re
import xml.etree.ElementTree as ET

def extract_svg(content):
    start = content.find("<svg")
    end = content.rfind("</svg>")
    if start < 0 or end < 0:
        return None, "no complete SVG tag", None
    svg = content[start:end + len("</svg>")]
    repairs = []
    # Some outputs try to draw a three-point path as a <line> with two x2/y2
    # pairs. XML rejects duplicate attributes. Preserve all three points.
    def three_point_line(match):
        x1, y1, x2, y2, x3, y3 = match.groups()
        return f'<polyline points="{x1},{y1} {x2},{y2} {x3},{y3}"/>'

    svg, line_count = re.subn(
        r'<line\s+x1="([^"]+)"\s+y1="([^"]+)"\s+x2="([^"]+)"\s+y2="([^"]+)"'
        r'\s+x2="([^"]+)"\s+y2="([^"]+)"\s*/>',
        three_point_line, svg,
    )
    if line_count:
        repairs.append(f"converted {line_count} duplicate-coordinate lines to polylines")
    try:
        root = ET.fromstring(svg)
        if not root.tag.endswith("svg"):
            return None, "XML root is not SVG", None
    except ET.ParseError as error:
        names = set(re.findall(r"&([A-Za-z][A-Za-z0-9]+);", svg))
        replaceable = names - {"amp", "lt", "gt", "quot", "apos"}
        if not replaceable or not replaceable.issubset(html.entities.name2codepoint):
            return None, f"SVG XML parse failed: {error}", None
        for name in replaceable:
            svg = svg.replace(f"&{name};", chr(html.entities.name2codepoint[name]))
        try:
            ET.fromstring(svg)
        except ET.ParseError as second_error:
            return None, f"SVG XML parse failed after named-entity repair: {second_error}", None
        repairs.append("decoded HTML named entities: " + ", ".join(sorted(replaceable)))
    return svg, None, "; ".join(repairs) if repairs else None
