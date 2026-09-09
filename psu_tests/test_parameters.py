import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

class CustomField:
    """Descriptor for declarative custom fields in tests"""
    def __init__(self, name: str, field_type: type, default: Any = None, choices: List[str] = None):
        self.name = name
        self.field_type = field_type
        self.default = default
        self.choices = choices

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name, self.default)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, self.field_type(value))

class BaseTestParameters:
    """
    Base class for declarative test parameters.
    Automatically serializes/deserializes itself.
    """
    def get_dict(self) -> Dict[str, Any]:
        """Auto-serialize all CustomField attributes and regular attributes."""
        res = {}
        # Simple serialization logic, can be expanded to match the legacy format if needed
        for key in dir(self):
            if not key.startswith('_') and not callable(getattr(self, key)):
                res[key] = getattr(self, key)
        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Auto-deserialize from a dict."""
        instance = cls()
        for k, v in data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
        return instance
