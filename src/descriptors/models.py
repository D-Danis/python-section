from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str) -> None:
        self.path = path.split(".")

    def __get__(self, instance: Model, owner: type) -> Any:
        if instance is None:
            return self
        value = instance.payload
        for key in self.path:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    break
            else:
                return None
        return value

    def __set__(self, instance: Model, value: Any) -> None:
        payload = instance.payload
        parts = self.path
        for key in parts[:-1]:
            if key not in payload or not isinstance(payload[key], dict):
                payload[key] = {}
            payload = payload[key]
        payload[parts[-1]] = value
