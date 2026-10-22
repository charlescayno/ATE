# run_simulation.bat — open & tried

## Can you open it?

**Yes.**

- **In Cursor:** opened `C:\Users\Charles\ATE\run_simulation.bat` (you can edit it there).
- **To run:** double-click in Explorer, or in cmd:
  ```bat
  C:\Users\Charles\ATE\run_simulation.bat
  ```

## Have I tried it?

**Yes (just now).** From this environment it started successfully:

```text
[INFO] Simulation mode — using C:\Users\Charles\.gemini\antigravity\scratch\ATE\conda_env\python.exe
```

Then `main.py -s` runs — the **PI ATE window** should appear on your desktop (check the taskbar if it is behind Cursor).

This clone has no local `conda_env`, so the batch file uses the **fallback** Python under `.gemini\antigravity\scratch\ATE\conda_env\`.

## If nothing appears

- Look for **PI ATE** on the taskbar / Alt+Tab.
- Run from cmd so you see errors:
  ```bat
  cd /d C:\Users\Charles\ATE
  run_simulation.bat
  ```
- If you see `[ERROR] No PI ATE conda env found`, copy `conda_env` into `C:\Users\Charles\ATE\` from your other ATE tree.

## Earlier check (headless)

Simulation was also verified with:

`conda_env\python.exe scripts\verify_manual_control_scope_estop.py`

That loads the same simulated equipment without needing you to click through the GUI.
