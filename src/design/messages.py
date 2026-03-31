import datetime
import enum
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol


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
    """Универсальное представление сообщения."""

    text: str
    sender: str
    channel: str
    timestamp: datetime
    raw_data: dict[str, Any] | None = field(default=None)


class Parser(Protocol):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        """Преобразует JsonMessage в ParsedMessage."""
        ...


class TelegramParser:
    def parse(self, message: JsonMessage) -> ParsedMessage:
        data = json.loads(message.payload)
        return ParsedMessage(
            text=data.get("text", ""),
            sender=data.get("from", {}).get("username", "unknown"),
            channel=str(data.get("chat", {}).get("id", "")),
            timestamp=datetime.fromtimestamp(data.get("date", 0)),
            raw_data=data,
        )


class MattermostParser:
    def parse(self, message: JsonMessage) -> ParsedMessage:
        data = json.loads(message.payload)
        return ParsedMessage(
            text=data.get("message", ""),
            sender=data.get("user_name", "unknown"),
            channel=data.get("channel_name", ""),
            timestamp=datetime.fromisoformat(
                data.get("create_at", "1970-01-01T00:00:00")
            ),
            raw_data=data,
        )


class SlackParser:
    def parse(self, message: JsonMessage) -> ParsedMessage:
        data = json.loads(message.payload)
        return ParsedMessage(
            text=data.get("text", ""),
            sender=data.get("user", "unknown"),
            channel=data.get("channel", ""),
            timestamp=datetime.fromtimestamp(float(data.get("ts", 0))),
            raw_data=data,
        )


class ParserFactory:
    def __init__(self):
        self._parsers: dict[MessageType, Parser] = {}

    def register(self, message_type: MessageType, parser: Parser) -> None:
        self._parsers[message_type] = parser

    def get_parser(self, message_type: MessageType) -> Parser:
        parser = self._parsers.get(message_type)
        if parser is None:
            raise ValueError(f"No parser registered for {message_type}")
        return parser


if __name__ == "__main__":
    factory = ParserFactory()

    # регистрируем парсеры
    factory.register(MessageType.TELEGRAM, TelegramParser())
    factory.register(MessageType.MATTERMOST, MattermostParser())
    factory.register(MessageType.SLACK, SlackParser())

    # Пример входного сообщения
    raw_json = '{"text": "Hello", "from": {"username": "alice"}, "chat": {"id": 123}, "date": 1700000000}'
    message = JsonMessage(message_type=MessageType.TELEGRAM, payload=raw_json)

    # Получаем парсер и преобразуем
    parser = factory.get_parser(message.message_type)
    parsed = parser.parse(message)

    print(parsed)
