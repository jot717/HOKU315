from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLAN = ROOT / "docs/active/governance/PHASE2B_CLOUD_PERSISTENCE_PLAN.md"

REQUIRED_SECTIONS = (
    "Local vs cloud ownership",
    "Auth boundaries",
    "Dual-write behavior",
    "Sync rules",
    "Conflict rules",
    "Failure handling",
    "Anti-desync",
    "no implementation",
)


def test_phase2b_plan_exists() -> None:
    assert PLAN.is_file()
    text = PLAN.read_text(encoding="utf-8")
    assert "PHASE2-B" in text
    for section in REQUIRED_SECTIONS:
        assert section.lower() in text.lower(), f"missing: {section}"
    assert "Supabase adapter implementation" in text or "no implementation" in text.lower()
    assert "db_service" in text
    assert "LocalStorage" in text


def test_cloud_backend_modules_exist() -> None:
    assert (ROOT / "product/persistence/runtime/cloud_backend.py").is_file()
    assert (ROOT / "product/persistence/runtime/dual_write_backend.py").is_file()
    assert (ROOT / "product/persistence/runtime/sync_status.py").is_file()
