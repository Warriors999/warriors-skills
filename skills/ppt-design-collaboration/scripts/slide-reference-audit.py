#!/usr/bin/env python3
"""Measure slide references and compare an approved visual master with a render.

Only Pillow is required. The script reports observable facts, not a claim of
semantic similarity:

  audit   palette shares, horizontal/vertical colour bands, and a calm-zone grid
  compare pixel drift between an approved image and a rendered PPTX page

Examples:
  python3 slide-reference-audit.py audit ref.png --out ./audit
  python3 slide-reference-audit.py compare approved.png rendered.png --out ./qa
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat


MAX_ANALYSIS_WIDTH = 1280
PALETTE_SIZE = 10
COLOUR_MERGE_TOLERANCE = 14
RESAMPLE_LANCZOS = getattr(
    getattr(Image, "Resampling", Image), "LANCZOS", Image.LANCZOS
)
DITHER_NONE = getattr(getattr(Image, "Dither", None), "NONE", 0)


def output_key(*paths: Path) -> str:
    identity = json.dumps([str(path.resolve()) for path in paths])
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
    return f"{paths[0].stem[:48]}-{digest}"


def load_rgb(path: Path) -> Image.Image:
    image = Image.open(path)
    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        rgba = image.convert("RGBA")
        canvas = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        canvas.alpha_composite(rgba)
        return canvas.convert("RGB")
    return image.convert("RGB")


def prepared(image: Image.Image) -> Image.Image:
    if image.width <= MAX_ANALYSIS_WIDTH:
        return image
    height = round(image.height * MAX_ANALYSIS_WIDTH / image.width)
    return image.resize((MAX_ANALYSIS_WIDTH, height), RESAMPLE_LANCZOS)


def hex_colour(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def palette_info(image: Image.Image) -> tuple[list[dict], Image.Image, dict[int, int]]:
    quantized = image.quantize(
        colors=PALETTE_SIZE, method=Image.MEDIANCUT, dither=DITHER_NONE
    )
    raw = quantized.getpalette() or []
    total = image.width * image.height
    entries = []
    for count, index in sorted(
        quantized.getcolors(maxcolors=total) or [], reverse=True
    ):
        entries.append((count, index, tuple(raw[index * 3 : index * 3 + 3])))

    families: list[dict] = []
    index_to_family: dict[int, int] = {}
    for count, index, rgb in entries:
        match = None
        for family_index, family in enumerate(families):
            distance = max(
                abs(rgb[channel] - family["rgb"][channel]) for channel in range(3)
            )
            if distance <= COLOUR_MERGE_TOLERANCE:
                match = family_index
                break
        if match is None:
            families.append(
                {
                    "rgb": rgb,
                    "pixels": count,
                    "members": 1,
                }
            )
            index_to_family[index] = len(families) - 1
        else:
            family = families[match]
            combined = family["pixels"] + count
            family["rgb"] = tuple(
                round(
                    (family["rgb"][channel] * family["pixels"] + rgb[channel] * count)
                    / combined
                )
                for channel in range(3)
            )
            family["pixels"] = combined
            family["members"] += 1
            index_to_family[index] = match

    old_to_new = {old: new for new, old in enumerate(
        sorted(range(len(families)), key=lambda item: families[item]["pixels"], reverse=True)
    )}
    families.sort(key=lambda item: item["pixels"], reverse=True)
    colours = [
        {
            "hex": hex_colour(family["rgb"]),
            "share_pct": round(family["pixels"] * 100 / total, 1),
            "pixels": family["pixels"],
            "merged_colours": family["members"],
        }
        for family in families
    ]
    index_to_family = {
        index: old_to_new[family_index]
        for index, family_index in index_to_family.items()
    }
    return colours, quantized, index_to_family


def colour_bands(
    quantized: Image.Image, palette: list[dict], index_to_family: dict[int, int], axis: str
) -> list[dict]:
    width, height = quantized.size
    indices = list(quantized.getdata())
    length = height if axis == "rows" else width
    spans = height if axis == "rows" else width
    dominant = []
    for position in range(length):
        if axis == "rows":
            line = indices[position * width : (position + 1) * width]
        else:
            line = [indices[row * width + position] for row in range(height)]
        counts = Counter(index_to_family[item] for item in line)
        index, count = counts.most_common(1)[0]
        dominant.append((index, count / spans))

    minimum = max(2, math.ceil(length * 0.025))
    runs: list[tuple[int, int, int]] = []
    start = None
    active = None
    for position, (index, share) in enumerate(dominant + [(None, 0.0)]):
        strong = share >= 0.55
        if strong and start is not None and index == active:
            continue
        if start is not None:
            if position - start >= minimum:
                runs.append((start, position, active))
            start, active = None, None
        if strong:
            start, active = position, index

    merged: list[dict] = []
    for start, end, index in runs:
        if (
            merged
            and merged[-1]["index"] == index
            and start - merged[-1]["end_px"] <= 1
        ):
            merged[-1]["end_px"] = end
            continue
        merged.append({"index": index, "start_px": start, "end_px": end})

    result = []
    for item in merged:
        result.append(
            {
                "colour": palette[item["index"]]["hex"],
                "start_pct": round(item["start_px"] * 100 / length, 1),
                "end_pct": round(item["end_px"] * 100 / length, 1),
                "thickness_pct": round(
                    (item["end_px"] - item["start_px"]) * 100 / length, 1
                ),
            }
        )
    return result


def calm_grid(image: Image.Image, columns: int, rows: int) -> dict:
    grey = image.convert("L")
    edges = grey.filter(ImageFilter.FIND_EDGES)
    cells = []
    for row in range(rows):
        line = []
        for column in range(columns):
            box = (
                column * edges.width // columns,
                row * edges.height // rows,
                (column + 1) * edges.width // columns,
                (row + 1) * edges.height // rows,
            )
            energy = ImageStat.Stat(edges.crop(box)).mean[0]
            if energy < 4:
                level = "calm"
            elif energy < 8:
                level = "low"
            elif energy < 16:
                level = "medium"
            else:
                level = "busy"
            line.append({"edge_energy": round(energy, 1), "level": level})
        cells.append(line)

    calm = {
        (row, column)
        for row, line in enumerate(cells)
        for column, cell in enumerate(line)
        if cell["level"] in ("calm", "low")
    }
    largest_block = None
    for row in range(rows - 1):
        for column in range(columns - 1):
            block = {
                (row, column),
                (row, column + 1),
                (row + 1, column),
                (row + 1, column + 1),
            }
            if block <= calm:
                largest_block = {
                    "x_pct": round(column * 100 / columns, 1),
                    "y_pct": round(row * 100 / rows, 1),
                    "width_pct": round(200 / columns, 1),
                    "height_pct": round(200 / rows, 1),
                }
                break
        if largest_block:
            break

    return {
        "columns": columns,
        "rows": rows,
        "cells": cells,
        "calm_cell_count": len(calm),
        "largest_calm_2x2_block": largest_block,
    }


def annotate(
    source: Image.Image, cells: list[list[dict]], rows: int, columns: int
) -> Image.Image:
    canvas = source.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas, "RGBA")
    for row in range(rows):
        for column in range(columns):
            x0 = column * canvas.width / columns
            y0 = row * canvas.height / rows
            x1 = (column + 1) * canvas.width / columns
            y1 = (row + 1) * canvas.height / rows
            level = cells[row][column]["level"]
            fill = {
                "calm": (40, 160, 90, 70),
                "low": (40, 160, 90, 35),
                "medium": (230, 170, 40, 45),
                "busy": (200, 50, 50, 55),
            }[level]
            draw.rectangle((x0, y0, x1, y1), fill=fill, outline=(255, 255, 255, 170))
    return canvas


def audit(path: Path, out_dir: Path, columns: int, rows: int) -> dict:
    original = load_rgb(path)
    image = prepared(original)
    palette, quantized, index_to_family = palette_info(image)
    grid = calm_grid(image, columns, rows)
    result = {
        "input": str(path),
        "size_px": [original.width, original.height],
        "aspect_ratio": round(original.width / original.height, 4),
        "palette": palette,
        "horizontal_bands": colour_bands(
            quantized, palette, index_to_family, "rows"
        ),
        "vertical_bands": colour_bands(
            quantized, palette, index_to_family, "columns"
        ),
        "calm_grid": grid,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = output_key(path)
    annotated = annotate(image, grid["cells"], rows, columns)
    annotated_path = out_dir / f"{stem}-audit.png"
    annotated.save(annotated_path)
    result["annotated_image"] = str(annotated_path)

    json_path = out_dir / f"{stem}-audit.json"
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result["json"] = str(json_path)
    return result


def compare(approved: Path, rendered: Path, out_dir: Path, threshold: int,
            normalize_resolution: bool = False) -> dict:
    left = load_rgb(approved)
    right = load_rgb(rendered)
    original_sizes = (left.size, right.size)
    if left.width * right.height != right.width * left.height:
        raise ValueError(f"aspect ratios differ: {left.size} vs {right.size}; comparison would distort the render")
    if right.size != left.size:
        if not normalize_resolution:
            raise ValueError("resolutions differ; use --normalize-resolution for proportional resampling")
        right = right.resize(left.size, RESAMPLE_LANCZOS)

    diff = ImageChops.difference(left, right)
    stat = ImageStat.Stat(diff)
    mean_abs = sum(stat.mean) / 3
    changed = sum(1 for pixel in diff.convert("L").getdata() if pixel > threshold)
    total = left.width * left.height

    columns, rows = 6, 4
    grid_diff = []
    for row in range(rows):
        line = []
        for column in range(columns):
            box = (
                column * left.width // columns,
                row * left.height // rows,
                (column + 1) * left.width // columns,
                (row + 1) * left.height // rows,
            )
            region = diff.crop(box)
            region_mean = sum(ImageStat.Stat(region).mean) / 3
            line.append(round(region_mean, 1))
        grid_diff.append(line)

    amplified = diff.point(lambda value: min(255, value * 3))
    side = Image.new("RGB", (left.width, left.height * 2 + 8), (255, 255, 255))
    side.paste(left, (0, 0))
    side.paste(right, (0, left.height + 8))

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = output_key(approved, rendered)
    diff_path = out_dir / f"{stem}-diff-amplified.png"
    side_path = out_dir / f"{stem}-side-by-side.png"
    amplified.save(diff_path)
    side.save(side_path)

    result = {
        "approved": str(approved),
        "rendered": str(rendered),
        "approved_original_size_px": list(original_sizes[0]),
        "rendered_original_size_px": list(original_sizes[1]),
        "approved_original_aspect_ratio": original_sizes[0][0] / original_sizes[0][1],
        "rendered_original_aspect_ratio": original_sizes[1][0] / original_sizes[1][1],
        "resolution_normalized": original_sizes[0] != original_sizes[1],
        "normalization": "rendered proportionally resampled to approved resolution" if original_sizes[0] != original_sizes[1] else "none",
        "size_px": [left.width, left.height],
        "mean_abs_difference_0_255": round(mean_abs, 2),
        "changed_pixel_pct": round(changed * 100 / total, 2),
        "threshold_0_255": threshold,
        "grid_mean_difference": grid_diff,
        "diff_image": str(diff_path),
        "side_by_side": str(side_path),
    }
    json_path = out_dir / f"{stem}-compare.json"
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result["json"] = str(json_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    audit_parser = sub.add_parser("audit", help="measure one or more reference images")
    audit_parser.add_argument("images", nargs="+", type=Path)
    audit_parser.add_argument("--out", type=Path, default=Path("./reference-audit"))
    audit_parser.add_argument("--columns", type=int, default=6)
    audit_parser.add_argument("--rows", type=int, default=4)

    compare_parser = sub.add_parser("compare", help="compare approved and rendered pages")
    compare_parser.add_argument("approved", type=Path)
    compare_parser.add_argument("rendered", type=Path)
    compare_parser.add_argument("--out", type=Path, default=Path("./compare"))
    compare_parser.add_argument("--threshold", type=int, default=12)
    compare_parser.add_argument("--normalize-resolution", action="store_true",
                                help="explicitly resample equal-aspect renders to the approved resolution")

    args = parser.parse_args()
    if args.command == "audit" and (args.columns < 1 or args.rows < 1):
        parser.error("columns and rows must be positive")
    if args.command == "compare" and not 0 <= args.threshold <= 255:
        parser.error("threshold must be between 0 and 255")
    if args.command == "audit":
        results = [audit(path, args.out, args.columns, args.rows) for path in args.images]
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(
            json.dumps(
                compare(args.approved, args.rendered, args.out, args.threshold,
                        args.normalize_resolution),
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
