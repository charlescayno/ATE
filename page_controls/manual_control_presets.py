"""Named Manual Equipment Control session presets (JSON on disk)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PRESETS_FILENAME = "manual_control_presets.json"
STORE_VERSION = 1


def presets_file(base_dir: Path | None = None) -> Path:
    root = base_dir if base_dir is not None else Path.cwd()
    return root / PRESETS_FILENAME


def empty_store() -> dict[str, Any]:
    return {"version": STORE_VERSION, "presets": {}}


def load_store(base_dir: Path | None = None) -> dict[str, Any]:
    path = presets_file(base_dir)
    if not path.is_file():
        return empty_store()
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[MANUAL] Presets read failed ({path}): {exc}")
        return empty_store()
    if not isinstance(data, dict):
        return empty_store()
    presets = data.get("presets")
    if not isinstance(presets, dict):
        data["presets"] = {}
    data.setdefault("version", STORE_VERSION)
    return data


def save_store(store: dict[str, Any], base_dir: Path | None = None) -> None:
    path = presets_file(base_dir)
    store = dict(store)
    store["version"] = STORE_VERSION
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(store, f, indent=2)
    except OSError as exc:
        print(f"[MANUAL] Presets write failed ({path}): {exc}")


def merge_imported_store(current: dict[str, Any], imported: Any) -> dict[str, Any]:
    """Merge presets from an exported file or single preset dict."""
    out = dict(current)
    presets = out.setdefault("presets", {})
    if not isinstance(presets, dict):
        presets = {}
        out["presets"] = presets
    if isinstance(imported, dict) and "presets" in imported and isinstance(imported["presets"], dict):
        for name, state in imported["presets"].items():
            if isinstance(name, str) and isinstance(state, dict):
                presets[name] = state
        return out
    if isinstance(imported, dict) and all(isinstance(v, dict) for v in imported.values()):
        for name, state in imported.items():
            if isinstance(name, str):
                presets[name] = state
    return out
