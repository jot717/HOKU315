# SPRINT — TARGET SIGNAL PROFILE v1

## STATUS

ACTIVE

## DEFINITION OF DONE

* Target constitution + flow + schema docs merged
* `target_profile_store` persists `runtime_state/target_profile.json`
* `/target` page saves target; insight uses target + `relationship_simulation_engine` for overlap
* Guardian copy leads with **object / interaction** framing when a target is named
* Memory records high-risk **target × pattern** tags
* `python ops/flow/check_all_flows.py` + `pytest tests/regression/` pass

## OUT OF SCOPE

SNS, vectors, cloud sync, multi-user graphs.
