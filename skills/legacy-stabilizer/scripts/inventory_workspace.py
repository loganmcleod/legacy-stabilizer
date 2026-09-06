#!/usr/bin/env python3
"""Discover repositories in a stabilization workspace and emit a JSON inventory.

Scope: topology only. This script reports what exists — repos, revisions, build
systems, and *likely* layer paths. It never classifies defects, never asserts a
call relationship, and never sets a finding status. Text matches are candidates
for an agent/human to corroborate, nothing more.

Usage:
    python inventory_workspace.py <workspace-dir> [--out inventory.json]

Output: JSON to stdout (or --out) with one entry per discovered repository.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Build-system signatures -> language/build label. Presence of the marker file
# at a repo root (or one level down for multi-module) is a candidate signal.
BUILD_MARKERS = {
    "pom.xml": "java/maven",
    "build.gradle": "java/gradle",
    "build.gradle.kts": "java/gradle",
    "nx.json": "javascript/nx",
    "angular.json": "javascript/angular",
    "package.json": "javascript/npm",
    "bower.json": "javascript/bower",
    "webpack.config.js": "javascript/webpack",
    "module-federation.config.js": "javascript/module-federation",
    "requirements.txt": "python/pip",
    "pyproject.toml": "python",
    "go.mod": "go",
}

# Likely-layer path hints. These are DIRECTORY-NAME heuristics only, used to
# point reviewers at candidate areas. They prove nothing about runtime roles.
LAYER_HINTS = {
    "presentation-angularjs": ["controllers", "directives", "webapp", "views"],
    "presentation-angular": ["apps", "libs", "components", "features", "app"],
    "presentation-react": ["components", "pages", "hooks", "features", "src"],
    "service-spring": ["service", "services", "controller", "web", "rest"],
    "persistence-sql": ["repository", "dao", "mapper", "mybatis", "sql", "domain"],
    "search-solr": ["solr", "search", "indexing"],
    "cache-redis": ["cache", "redis"],
}

# Extensions worth counting to hint at the dominant stack, cheaply.
COUNT_EXTS = [".java", ".js", ".jsx", ".ts", ".tsx", ".html", ".sql", ".xml"]

SKIP_DIRS = {".git", "node_modules", "target", "build", "dist", ".idea", "__pycache__"}


def git(repo: Path, *args) -> str:
    """Run a git command in repo; return stripped stdout or '' on failure."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=15,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def find_repos(workspace: Path) -> list:
    """A repo is a git working tree, or (fallback) any top-level dir with a
    build marker. Nested git repos are each reported."""
    repos = []
    if (workspace / ".git").exists():
        repos.append(workspace)
    for child in sorted(workspace.iterdir()):
        if not child.is_dir() or child.name in SKIP_DIRS:
            continue
        if (child / ".git").exists():
            repos.append(child)
        elif any((child / m).exists() for m in BUILD_MARKERS):
            repos.append(child)
    return repos or ([workspace] if any(workspace.iterdir()) else [])


def detect_builds(repo: Path) -> list:
    """Marker files found at root or one directory deep (multi-module)."""
    found = set()
    for marker, label in BUILD_MARKERS.items():
        if (repo / marker).exists():
            found.add(label)
        else:
            for child in repo.iterdir():
                if child.is_dir() and child.name not in SKIP_DIRS and (child / marker).exists():
                    found.add(label)
                    break
    return sorted(found)


def detect_layers(repo: Path) -> dict:
    """Map layer -> candidate relative paths whose dir name matches a hint."""
    hits = {layer: [] for layer in LAYER_HINTS}
    for root, dirs, _ in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, repo)
        name = os.path.basename(root).lower()
        for layer, hints in LAYER_HINTS.items():
            if name in hints and rel != ".":
                hits[layer].append(rel)
    return {k: sorted(set(v))[:20] for k, v in hits.items() if v}


def count_exts(repo: Path) -> dict:
    counts = {e: 0 for e in COUNT_EXTS}
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in counts:
                counts[ext] += 1
    return {k: v for k, v in counts.items() if v}


def inventory_repo(repo: Path) -> dict:
    sha = git(repo, "rev-parse", "HEAD") or "unknown"
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD") or "unknown"
    return {
        "repo": repo.name,
        "path": str(repo.resolve()),
        "sha": sha,
        "default_branch": branch,
        "build_systems": detect_builds(repo) or ["unknown"],
        "file_counts": count_exts(repo),
        "candidate_layers": detect_layers(repo),
        # Fields the agent/human must fill — never guessed here.
        "deployables": "unknown",
        "database_schemas": "unknown",
        "owner": "unknown",
        "production_criticality": "unknown",
    }


def build_inventory(workspace: Path) -> dict:
    repos = find_repos(workspace)
    return {
        "workspace": str(workspace.resolve()),
        "repository_count": len(repos),
        "repositories": [inventory_repo(r) for r in repos],
        "note": "Topology only. Layer paths are name heuristics, not proof of runtime role.",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("workspace", help="Directory containing one or more repositories")
    ap.add_argument("--out", help="Write JSON here instead of stdout")
    args = ap.parse_args(argv)

    ws = Path(args.workspace)
    if not ws.is_dir():
        print(f"error: {ws} is not a directory", file=sys.stderr)
        return 2

    data = build_inventory(ws)
    text = json.dumps(data, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(f"wrote {args.out} ({data['repository_count']} repos)", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
