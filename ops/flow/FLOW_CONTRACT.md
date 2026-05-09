# FLOW CONTRACT v1

Every product flow MUST contain:

- README.md
- state_model.md
- product_flow.md
- runtime/
- tests/regression/

---

## REQUIRED FLOW STRUCTURE

product/<flow>/

    README.md
    state_model.md
    product_flow.md

    runtime/
        __init__.py
        *_engine.py
        *_flow.py

---

## REQUIRED REGRESSION

tests/regression/

    test_<flow>_flow.py

---

## REQUIRED PROCESS

BACKLOG
→ SPRINT
→ IMPLEMENT
→ REGRESSION
→ DONE
