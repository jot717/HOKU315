"""Regression for FLOW INTEGRATION (`core` registry); logic shared with test_flow_integration."""

from __future__ import annotations

from tests.regression.test_flow_integration import _assert_full_flow


def test_core_full_flow() -> None:
    _assert_full_flow()
