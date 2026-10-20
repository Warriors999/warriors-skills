#!/usr/bin/env python3
"""Deterministic smoke checks for the Jimeng prompt reference skill package."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCES = ROOT / "references.md"
MODEL_REGISTRY = ROOT / "references" / "model-registry.md"
JIMENG_REFERENCE = ROOT / "references" / "jimeng-seedance-2.5.md"
EVALS = ROOT / "evals" / "evals.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    references = REFERENCES.read_text(encoding="utf-8")
    model_registry = MODEL_REGISTRY.read_text(encoding="utf-8")
    jimeng_reference = JIMENG_REFERENCE.read_text(encoding="utf-8")
    evals = json.loads(EVALS.read_text(encoding="utf-8"))

    if not re.search(r"^name: jimeng-prompt-reference-skill$", skill, re.MULTILINE):
        fail("frontmatter name is missing")
    if not re.search(r"^description: Use when .+", skill, re.MULTILINE):
        fail("description must start with 'Use when'")

    required_terms = {
        "evidence ladder": "evidence ladder",
        "route before writing": "mode routing",
        "素材角色": "reference role routing",
        "首尾帧": "first/last-frame routing",
        "official-derived foundation": "official-derived foundation",
        "正向描述": "positive description layer",
        "反向描述": "negative description layer",
        "潜台词": "subtext layer",
        "标注工具与方位": "annotation routing",
        "error-prevention lint": "error prevention",
        "Alpha": "alpha limitation",
        "一次只改一个变量": "one-variable iteration",
    }
    lower_skill = skill.lower()
    for term, label in required_terms.items():
        if term.lower() not in lower_skill:
            fail(f"missing {label}: {term}")

    if "Square-Zero-Labs/video-prompting-skill" not in references:
        fail("external video skill provenance is not recorded")
    if "不迁移" not in references:
        fail("non-transferable platform rules are not recorded")
    for term in ("即梦", "unknown", "portable", "Alpha"):
        if term not in model_registry:
            fail(f"model registry is missing: {term}")
    for term in (
        "第 3 章",
        "素材描述",
        "一句话概述",
        "正向描述",
        "反向描述",
        "表演核心",
        "潜台词",
        "标注工具与方位",
        "粗颗粒度",
        "细颗粒度",
        "未核验能力边界",
    ):
        if term not in jimeng_reference:
            fail(f"Jimeng reference is missing: {term}")

    if evals.get("skill_name") != "jimeng-prompt-reference-skill":
        fail("eval skill name is incorrect")
    cases = evals.get("evals", [])
    if len(cases) < 4:
        fail("at least four regression cases are required")
    for case in cases:
        if not case.get("assertions"):
            fail(f"eval {case.get('id')} has no assertions")

    print("PASS: jimeng-prompt-reference-skill package smoke checks")


if __name__ == "__main__":
    main()
