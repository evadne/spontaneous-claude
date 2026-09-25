"""Create compact 5×5 contact sheets for visual audit of every seed."""

import argparse
import json
import subprocess
from pathlib import Path

from visible_svg_text import claude_literal


def run(command):
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"{' '.join(map(str, command))}: {result.stderr[-1000:]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    tiles = args.output / "tiles"
    tiles.mkdir(exist_ok=True)
    files = []
    for file in sorted(args.processed.glob("*/classification.json")):
        record = json.loads(file.read_text())
        name = record["id"]
        svg_literal, _ = claude_literal(file.parent / "portrait.svg")
        positive = bool(record["reasoning_judge"]["claude_self"] or
                        (record["image_judge"] or {}).get("clear_claude_identity") or
                        svg_literal)
        uncertain = bool(record["reasoning_judge"]["uncertain"] or
                         (record["image_judge"] or {}).get("uncertain"))
        colour = "#d95c3a" if positive else ("#d6ad44" if uncertain else "#d2ccc3")
        image = file.parent / "portrait.png"
        tile = tiles / f"{name}.png"
        source = str(image) if image.exists() else "xc:#eceae6"
        command = ["magick"]
        if image.exists():
            command += [source, "-resize", "256x256", "-background", "#eceae6",
                        "-gravity", "center", "-extent", "256x256"]
        else:
            command += ["-size", "256x256", source, "-font", "/System/Library/Fonts/Supplemental/Arial.ttf",
                        "-pointsize", "14", "-fill", "#555555", "-gravity", "center",
                        "-annotate", "+0+0", "No rendered SVG"]
        command += ["-bordercolor", colour, "-border", "3",
                    "-background", "#f5f3ef", "-gravity", "south", "-splice", "0x30",
                    "-font", "/System/Library/Fonts/Supplemental/Arial.ttf", "-pointsize", "12", "-fill", "#222222",
                    "-annotate", "+0+7", f"{name} · {record['seed']}", str(tile)]
        run(command)
        files.append(tile)
    for start in range(0, len(files), 25):
        group = files[start:start + 25]
        destination = args.output / f"sheet-{start // 25 + 1:02d}.png"
        run(["magick", "montage", *map(str, group), "-font",
             "/System/Library/Fonts/Supplemental/Arial.ttf", "-tile", "5x5",
             "-geometry", "+5+5", "-background", "#f5f3ef", str(destination)])
    print(f"Built {len(files)} tiles and {(len(files) + 24) // 25} contact sheets")


if __name__ == "__main__":
    main()
