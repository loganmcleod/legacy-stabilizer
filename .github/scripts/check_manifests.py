#!/usr/bin/env python3
"""Lightweight manifest + frontmatter sanity check for CI.

Runs without the Claude Code CLI (which needs a network install and auth), so CI
stays fast and self-contained. It checks the things a broken publish would trip on:
valid manifest JSON with required fields, and a description in every skill, command,
and agent front matter. Run `claude plugin validate . --strict` locally for the full
schema check.

Exit 0 if everything looks well-formed, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []


def err(msg):
    errors.append(msg)


def check_json(path: Path, required: list):
    if not path.exists():
        err(f"{path.relative_to(ROOT)}: missing")
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        err(f"{path.relative_to(ROOT)}: invalid JSON ({e})")
        return None
    for key in required:
        if key not in data:
            err(f"{path.relative_to(ROOT)}: missing required key '{key}'")
    return data


def frontmatter(path: Path) -> dict:
    """Parse a minimal `key: value` YAML front-matter block (stdlib only)."""
    text = path.read_text()
    if not text.startswith("---"):
        err(f"{path.relative_to(ROOT)}: no front matter")
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        err(f"{path.relative_to(ROOT)}: unterminated front matter")
        return {}
    fields = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-", "#")):
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip()
    return fields


def require_description(path: Path):
    fm = frontmatter(path)
    if fm and not fm.get("description"):
        err(f"{path.relative_to(ROOT)}: front matter needs a 'description'")


# 1. Plugin + marketplace manifests.
check_json(ROOT / ".claude-plugin" / "plugin.json", ["name"])
mkt = check_json(ROOT / ".claude-plugin" / "marketplace.json", ["name", "plugins"])
if mkt:
    for i, p in enumerate(mkt.get("plugins", [])):
        for key in ("name", "source"):
            if key not in p:
                err(f"marketplace.json: plugins[{i}] missing '{key}'")

# 2. Skill, commands, agents all carry a description.
for skill in ROOT.glob("skills/*/SKILL.md"):
    require_description(skill)
for cmd in ROOT.glob("commands/*.md"):
    require_description(cmd)
for agent in ROOT.glob("agents/*.md"):
    fm = frontmatter(agent)
    for key in ("name", "description"):
        if fm and not fm.get(key):
            err(f"{agent.relative_to(ROOT)}: agent front matter needs '{key}'")

if errors:
    for e in errors:
        print(f"FAIL  {e}", file=sys.stderr)
    sys.exit(1)
print("manifests + front matter OK")
