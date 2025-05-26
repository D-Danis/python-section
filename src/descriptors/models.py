from functools import cached_property
from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON) -> None:
        self.payload = payload


class Field:
    def __init__(self, path: str) -> None:
        self.__path = path

    def __str__(self) -> str:
        return self.__path

    def __get__(self, instance, owner=None):
        wrapper = self.get_value_wrapper(payload=instance.payload, path=self.path)
        return wrapper.get(self.key, None)

    def __set__(self, instance, value):
        wrapper = self.get_value_wrapper(payload=instance.payload, path=self.path)
        wrapper[self.key] = value

    @property
    def path(self) -> str:
        return self.__path

    @cached_property
    def key(self) -> str:
        return self.path.split(".")[-1]

    def get_value_wrapper(self, payload: dict, path: str) -> JSON:
        keys = path.split(".")

        if len(keys) == 1:
            return payload

        payload.setdefault(keys[0], dict())

        if len(keys) == 2:
            return payload[keys[0]]

        return self.get_value_wrapper(payload[keys[0]], ".".join(keys[1:]))
