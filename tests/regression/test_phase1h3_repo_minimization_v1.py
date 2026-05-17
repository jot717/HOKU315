from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ACTIVE_ROUTES = (
    'route="/"',
    'route="/profile"',
    'route="/quiz"',
    'route="/target"',
    'route="/insight"',
    'route="/match"',
    'route="/login"',
)

DEAD_ROUTES = (
    'route="/chat"',
    'route="/story"',
    'route="/unlocks"',
)


def test_active_surface_map_exists() -> None:
    p = ROOT / "docs/active/product/ACTIVE_SURFACE_MAP.md"
    text = p.read_text(encoding="utf-8")
    assert p.is_file()
    assert "/profile" in text and "/match" in text


def test_only_active_routes_registered() -> None:
    src = (ROOT / "fox_quiz/fox_quiz.py").read_text(encoding="utf-8")
    for route in ACTIVE_ROUTES:
        assert route in src, route
    for dead in DEAD_ROUTES:
        assert dead not in src, dead


def test_dead_route_reference_archived() -> None:
    ref = ROOT / "docs/archive/dead_routes"
    for name in ("story_page.py", "chat_component.py", "unlocks_page.py"):
        assert (ref / name).is_file(), name


def test_archive_buckets_no_loose_md() -> None:
    root_md = [p for p in (ROOT / "docs/archive").glob("*.md")]
    assert len(root_md) == 1 and root_md[0].name == "README.md"
    assert (ROOT / "docs/archive/product").is_dir()
    assert (ROOT / "docs/archive/uat").is_dir()
    assert (ROOT / "docs/archive/hotfix").is_dir()


def test_runtime_templates_only() -> None:
    assert (ROOT / "runtime_state/templates/sample_profile.json").is_file()
    assert (ROOT / "runtime_state/templates/sample_target.json").is_file()
    for name in (
        "target_profile.json",
        "user_profile.json",
        "fox_memory.json",
        "session_history.json",
        "local_session.json",
    ):
        assert not (ROOT / "runtime_state" / name).exists(), name


def test_wip_quarantine_exists() -> None:
    assert (ROOT / "wip/README.md").is_file()
    assert not (ROOT / "product/shell").exists()
    assert (ROOT / "docs/active/product/PRODUCT_MASTER.md").is_file()
