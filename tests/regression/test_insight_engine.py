"""INSIGHT ENGINE v1 regression (same assertions as test_insight_flow)."""

from __future__ import annotations

from tests.regression.test_insight_flow import _assert_dynamic_insight


def test_dynamic_insight() -> None:
    _assert_dynamic_insight()
