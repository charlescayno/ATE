"""Verify Add Test load range table is configured for in-cell editing."""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADD_TEST = ROOT / "page_controls" / "add_test.py"
UI_MAIN = ROOT / "ui" / "ui_main.py"

REQUIRED_IN_ADD_TEST = (
    "_configure_load_range_table_editing",
    "load_range_table_item_changed",
    "_editable_load_range_table_item",
    "AllEditTriggers",
    "_edit_load_range_table_cell",
)

def main() -> int:
    add_text = ADD_TEST.read_text(encoding="utf-8")
    ui_text = UI_MAIN.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_IN_ADD_TEST if s not in add_text]
    if missing:
        print("FAIL add_test.py missing:", ", ".join(missing))
        return 1
    if "AllEditTriggers" not in ui_text or "table_add_tests_load_range.setEditTriggers" not in ui_text:
        print("FAIL ui_main.py load range table still read-only")
        return 1
    ast.parse(add_text)
    print("OK load range editing hooks present in:")
    print(" ", ADD_TEST)
    print(" ", UI_MAIN)
    return 0

if __name__ == "__main__":
    sys.exit(main())
