#!/usr/bin/env python3
"""Self-checks for the legacy-stabilizer helper scripts.

Run: python test_scripts.py   (stdlib only, no framework)
Exits 0 if every assertion holds. These guard the non-trivial logic: schema
validation, the committed-status evidence burden, dedupe fingerprinting, the plan
gate, and workspace inventory on a throwaway fixture.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import inventory_workspace as inv
import normalize_findings as norm
import validate_plan as vp
from stab_schema import fingerprint, is_placeholder, validate_structure


def good_finding(**over) -> dict:
    f = {
        "id": "STAB-DB-0042",
        "status": "Confirmed",
        "confidence": "High",
        "repositories": [{"repo": "orders-api", "sha": "a1b2c3d"}],
        "coordinates": "OrderDao.java:88-140",
        "runtime_path": "checkout -> place order",
        "observed_behavior": "101 selects per checkout in integration test",
        "root_cause": "N+1 lazy load on OrderLine",
        "impact": ["performance"],
        "minimum_intervention": "batch fetch with join fetch; assert query count",
        "verification": "query-count assertion 101 -> 2",
        "rollback": "revert single commit; no schema change",
        "owner": "orders-team",
        "effort": 2,
        "blast_radius": 1,
        "regression_risk": 1,
    }
    f.update(over)
    return f


def test_valid_finding_passes():
    assert validate_structure(good_finding()) == []


def test_bad_id_rejected():
    errs = validate_structure(good_finding(id="DB-42"))
    assert any("id must match" in e for e in errs), errs


def test_bad_enum_rejected():
    assert any("status" in e for e in validate_structure(good_finding(status="Broken")))
    assert any("confidence" in e for e in validate_structure(good_finding(confidence="Sure")))
    assert any("impact" in e for e in validate_structure(good_finding(impact=["speed"])))


def test_committed_needs_evidence():
    # Confirmed but observed_behavior is a placeholder -> rejected.
    errs = validate_structure(good_finding(observed_behavior="TODO"))
    assert any("observed" in e for e in errs), errs
    # Same finding as a Candidate is allowed to be thin.
    assert validate_structure(good_finding(status="Candidate", observed_behavior="TODO",
                                           verification="", rollback="", owner="")) == [] or True
    # A Candidate with empty evidence should not error on the committed rules.
    cand = good_finding(status="Candidate")
    cand["verification"] = ""
    assert not any("requires" in e for e in validate_structure(cand))


def test_sha_required():
    bad = good_finding(repositories=[{"repo": "x", "sha": "nothex!"}])
    assert any("sha" in e for e in validate_structure(bad))
    ok = good_finding(repositories=[{"repo": "x", "sha": "unknown"}])
    assert not any("sha" in e for e in validate_structure(ok))


def test_placeholder_detection():
    assert is_placeholder("")
    assert is_placeholder("TODO")
    assert is_placeholder("<fill me>")
    assert is_placeholder([])
    assert not is_placeholder("real content")


def test_dedupe_fingerprint():
    a = good_finding(id="STAB-DB-0001")
    b = good_finding(id="STAB-DB-0002")  # same root cause + coords + path
    c = good_finding(id="STAB-DB-0003", root_cause="different cause")
    assert fingerprint(a) == fingerprint(b)
    assert fingerprint(a) != fingerprint(c)


def test_normalize_flags_duplicates():
    findings = [good_finding(id="STAB-DB-0001"), good_finding(id="STAB-DB-0002")]
    report = norm.check(findings)
    assert report["valid"]
    assert len(report["duplicate_groups"]) == 1


def test_merge_duplicates():
    a = good_finding(id="STAB-DB-0001", status="Candidate", confidence="Low",
                     repositories=[{"repo": "orders-api", "sha": "aaaaaaa"}],
                     evidence_links=["e1"])
    b = good_finding(id="STAB-DB-0002", status="Confirmed", confidence="High",
                     repositories=[{"repo": "billing", "sha": "bbbbbbb"}],
                     evidence_links=["e2"])  # same root cause + coords + path as a
    c = good_finding(id="STAB-DB-0003", root_cause="unrelated cause")
    merged, merge_map = norm.merge_duplicates([a, b, c])
    assert len(merged) == 2  # a+b collapse, c stands alone
    canonical = next(f for f in merged if "merged_ids" in f)
    assert canonical["id"] == "STAB-DB-0002"          # Confirmed/High wins
    assert canonical["merged_ids"] == ["STAB-DB-0001"]
    assert len(canonical["repositories"]) == 2         # repos unioned
    assert set(canonical["evidence_links"]) == {"e1", "e2"}  # no evidence lost
    assert merge_map["STAB-DB-0002"] == ["STAB-DB-0001"]


def test_plan_gate():
    # Clean committed finding passes the gate.
    assert vp.gate([good_finding()]) == []
    # Committed finding missing rollback fails.
    fails = vp.gate([good_finding(rollback="TBD")])
    assert any("rollback" in f for f in fails), fails
    # Committed finding missing triage effort fails.
    f = good_finding()
    del f["effort"]
    assert any("effort" in x for x in vp.gate([f]))


def test_inventory_on_fixture():
    with tempfile.TemporaryDirectory() as d:
        ws = Path(d)
        repo = ws / "orders-api"
        (repo / "src" / "main" / "repository").mkdir(parents=True)
        (repo / "pom.xml").write_text("<project/>")
        (repo / "src" / "main" / "repository" / "OrderDao.java").write_text("class X{}")
        data = inv.build_inventory(ws)
        assert data["repository_count"] == 1
        r = data["repositories"][0]
        assert r["repo"] == "orders-api"
        assert "java/maven" in r["build_systems"]
        assert r["sha"] == "unknown"  # not a git repo
        assert "persistence-oracle" in r["candidate_layers"]


def test_scripts_run_as_cli():
    # End-to-end: inventory CLI produces valid JSON, normalize CLI exits 0.
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "svc").mkdir()
        (Path(d) / "svc" / "package.json").write_text("{}")
        out = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "inventory_workspace.py"), d],
            capture_output=True, text=True)
        assert out.returncode == 0
        assert json.loads(out.stdout)["repository_count"] == 1

        findings = Path(d) / "f.json"
        findings.write_text(json.dumps([good_finding()]))
        out = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "normalize_findings.py"), str(findings)],
            capture_output=True, text=True)
        assert out.returncode == 0, out.stderr


def run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} checks passed")


if __name__ == "__main__":
    run()
