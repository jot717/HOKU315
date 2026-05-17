from __future__ import annotations

from product.match.runtime.match_rhythm_engine import generate_match_credibility_bundle


def test_match_flow_credibility_bundle_shape() -> None:
    bundle = generate_match_credibility_bundle(
        distance=0.35,
        compat_bucket="medium",
    )
    assert isinstance(bundle, dict)
    assert bundle.get("interaction_rhythm_line") or bundle.get("scenario_line")
