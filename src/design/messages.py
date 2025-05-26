from __future__ import annotations

import abc
import enum
from dataclasses import dataclass

__all__ = (
    "MessageType",
    "JsonMessage",
    "ParsedMessage",
    "TelegramMessage",
    "MattermostMessage",
    "SlackMessage",
    "message_factory",
)


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class ParserFactory:
    def __init__(self):
        self.__registry = {}

    def register(self, message_type: MessageType):
        def decorator(target_class):
            self.__registry[message_type] = target_class
            return target_class

        return decorator

    def get(self, message_type: MessageType) -> MessageParser:
        return self.__registry[message_type]


message_factory = ParserFactory()


class MessageParser(abc.ABC):
    def __init__(self, message: JsonMessage) -> None:
        self.message = message

    @abc.abstractmethod
    def parse(self) -> ParsedMessage:
        pass


@message_factory.register(message_type=MessageType.TELEGRAM)
class TelegramMessage(MessageParser):
    def parse(self) -> ParsedMessage:
        pass


@message_factory.register(message_type=MessageType.MATTERMOST)
class MattermostMessage(MessageParser):
    def parse(self) -> ParsedMessage:
        pass


@message_factory.register(message_type=MessageType.SLACK)
class SlackMessage(MessageParser):
    def parse(self) -> ParsedMessage:
        pass
