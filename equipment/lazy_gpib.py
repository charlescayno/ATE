"""Deferred VISA open for assumed GPIB addresses (e.g. locked at scan time)."""
from __future__ import annotations

import pyvisa
from pyvisa.errors import VisaIOError


class LazyGPIBDevice:
    """Opens the VISA session on first query/write; closes like a normal Resource."""

    def __init__(self, resource_manager: pyvisa.ResourceManager, resource_name: str):
        self._rm = resource_manager
        self.resource_name = (resource_name or "").strip()
        if not self.resource_name.upper().endswith("::INSTR"):
            self.resource_name = f"{self.resource_name}::INSTR"
        self._base_addr = self.resource_name.rsplit("::", 1)[0]
        self._dev = None
        self._timeout_ms = 5000

    @property
    def timeout(self):
        return self._timeout_ms

    @timeout.setter
    def timeout(self, value):
        self._timeout_ms = int(value)
        if self._dev is not None:
            self._dev.timeout = self._timeout_ms

    def _ensure_open(self):
        if self._dev is not None:
            return self._dev
        self._dev = self._rm.open_resource(self._base_addr)
        self._dev.timeout = self._timeout_ms
        return self._dev

    def query(self, command: str) -> str:
        return self._ensure_open().query(command)

    def write(self, command: str):
        return self._ensure_open().write(command)

    def read_raw(self):
        return self._ensure_open().read_raw()

    def read(self):
        return self._ensure_open().read()

    def clear(self):
        if self._dev is not None:
            self._dev.clear()

    def close(self):
        if self._dev is not None:
            try:
                self._dev.close()
            except Exception:
                pass
            self._dev = None
