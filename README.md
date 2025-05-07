# Chain-test-dev

## 2025.05.07
- `backup_test_chain.py` is an updated version of `test_chain.py`, but at one point the development went in a somewhat different direction, and `chain.py` is the main chain script now.
- `*.ui` are QT Designer files.
- `ui_*.py` are auto-generated from the corresponding `*.ui` files.
- `gui.py` is the main GUI file
- `report_actions.py` is for generating a json report
- `bombard_action.py` is a script for running as many `cline transfer` as possible
- `logger.py` icontains a singleton logger that is used across all other scripts
