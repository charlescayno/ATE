"""Regression: I2C UI widget lists must exist when test type combobox fires index changed."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from PySide2.QtWidgets import QApplication  # noqa: E402

app = QApplication.instance() or QApplication(sys.argv)

g = runpy.run_path(str(ROOT / "main.py"), run_name="__i2c_init__")
window = g["MainWindow"]()
add = window.add_test_pagehandler

errors = []


def check(name, ok, detail=""):
    if ok:
        print(f"OK  {name}")
    else:
        print(f"FAIL {name} {detail}")
        errors.append(name)


check(
    "init: i2c_ui_lineedit_frames after MainWindow",
    hasattr(add, "i2c_ui_lineedit_frames") and len(add.i2c_ui_lineedit_frames) == 10,
)

from psu_tests.test_type import TestTypes  # noqa: E402

for idx, tc in enumerate(TestTypes):
    needs_i2c = (tc.title in add.i2c_tests_names) or hasattr(tc, "i2c_ui_definitions")
    if not needs_i2c:
        continue
    add.ui.cbx_add_tests_testtype.setCurrentIndex(idx)
    add.test_type_index_changed()
    app.processEvents()
    check(f"switch: {tc.title}", hasattr(add, "i2c_ui_lineedit_frames"))

if errors:
    print(f"\n{len(errors)} check(s) failed.")
    sys.exit(1)
print("\nAll checks passed.")
