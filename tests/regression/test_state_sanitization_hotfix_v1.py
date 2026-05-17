from __future__ import annotations

import ast
from pathlib import Path

from fox_quiz.state import app_state as app_state_mod
from fox_quiz.ui.insight_panel import insight_panel
from fox_quiz.ui.pages.target_page import target_page

ROOT = Path(__file__).resolve().parents[2]


def test_hotfix_docs_exist() -> None:
    for rel in (
        "backlog/archive/BACKLOG_STATE_SANITIZATION_HOTFIX_v1.md",
        "backlog/archive/SPRINT_STATE_SANITIZATION_HOTFIX_v1.md",
        "docs/deprecated/archive/uat/STATE_SANITIZATION_RUNTIME_UAT.md",
    ):
        assert (ROOT / rel).is_file(), rel


def test_str_list_and_match_score_helpers() -> None:
    assert app_state_mod._str_list(None, limit=3) == []
    assert app_state_mod._str_list([" x ", 1, "x"], limit=5) == ["x", "1", "x"]
    assert app_state_mod._match_score_from_flow({}) == 0.0
    assert app_state_mod._match_score_from_flow({"match": {"score": 44.2}}) == 44.2
    assert app_state_mod._match_score_from_flow({"match": "bad"}) == 0.0


def test_dead_computed_vars_removed_from_source() -> None:
    src = (ROOT / "fox_quiz" / "state" / "app_state.py").read_text(encoding="utf-8")
    for dead in (
        "def insight_ai_summary",
        "def insight_shared_traits_text",
        "def insight_activity_analysis",
        "def signal_risk_flag_lines",
        "def guardian_presence_line_primary",
    ):
        assert dead not in src, dead


def test_app_state_rx_var_return_annotations_are_safe() -> None:
    """@rx.var return hints must be JSON-serializable primitive types (no dict/tuple)."""
    allowed = {"str", "int", "float", "bool"}
    path = ROOT / "fox_quiz" / "state" / "app_state.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name != "AppState":
            continue
        for item in node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            if not _has_rx_var_decorator(item):
                continue
            ann = _annotation_to_simple(item.returns)
            assert ann, f"missing return annotation on {item.name}"
            assert "dict" not in ann.lower() and "tuple" not in ann.lower(), item.name
            assert ann in allowed or ann == "List[str]" or ann == "list[str]", (
                f"{item.name} -> {ann}"
            )
        break
    else:
        raise AssertionError("AppState class not found")


def _has_rx_var_decorator(fn: ast.FunctionDef) -> bool:
    for dec in fn.decorator_list:
        if isinstance(dec, ast.Call):
            func = dec.func
            if isinstance(func, ast.Attribute) and func.attr == "var":
                if isinstance(func.value, ast.Name) and func.value.id == "rx":
                    return True
    return False


def _annotation_to_simple(node: ast.expr | None) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Subscript):
        base = _annotation_to_simple(node.value)
        if isinstance(node.slice, ast.Name):
            return f"{base}[{node.slice.id}]"
        if isinstance(node.slice, ast.Tuple):
            inner = ",".join(_annotation_to_simple(elt) for elt in node.slice.elts)
            return f"{base}[{inner}]"
        return f"{base}[?]"
    return ""


def test_insight_and_target_pages_compile() -> None:
    assert insight_panel() is not None
    assert target_page() is not None
