"""Fallback *IDN? strings when query fails or returns garbage (bench-specific)."""

from __future__ import annotations

import os
import re

# Full VISA resource name -> SCPI *IDN? response (Manufacturer,Model,Serial,FW)
_DEFAULT_ASSUMPTIONS: dict[str, str] = {
    "GPIB0::7::INSTR": "YOKOGAWA,WT310E,ASSUMED-GPIB7,0.0",
    "GPIB0::12::INSTR": "YOKOGAWA,760202,ASSUMED-GPIB12,0.0",  # WT500 family
}

# Manufacturer,Model,... — allow punctuation in manufacturer (e.g. "Magna-Power Electronics Inc.")
_VALID_IDN_RE = re.compile(r"^[^,\r\n]+,[^,\r\n]+,.+")


def _enabled() -> bool:
    return os.environ.get("PI_ATE_DISABLE_GPIB_IDN_ASSUME", "").strip().lower() not in (
        "1",
        "yes",
        "true",
    )


def assumed_idn_for(resource_name: str) -> str | None:
    if not _enabled():
        return None
    key = (resource_name or "").strip()
    if key in _DEFAULT_ASSUMPTIONS:
        return _DEFAULT_ASSUMPTIONS[key]
    # Allow GPIB0::7 without ::INSTR suffix
    if not key.endswith("::INSTR") and f"{key}::INSTR" in _DEFAULT_ASSUMPTIONS:
        return _DEFAULT_ASSUMPTIONS[f"{key}::INSTR"]
    return None


def assumed_model_for(resource_name: str) -> str | None:
    idn = assumed_idn_for(resource_name)
    if not idn:
        return None
    parts = idn.split(",", 3)
    return parts[1].strip() if len(parts) > 1 else None


def idn_looks_valid(device_id: str) -> bool:
    text = (device_id or "").strip()
    if len(text) < 8 or text.count(",") < 2:
        return False
    if not _VALID_IDN_RE.match(text):
        return False
    # Reject obvious bus garbage (non-printable / too many symbols)
    printable = sum(1 for c in text if c.isprintable() and c not in "\x7f")
    return printable >= len(text) * 0.95
