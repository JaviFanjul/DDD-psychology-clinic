from dataclasses import dataclass
from enum import StrEnum


class MessageType(StrEnum):
    PATIENT = "patient"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, object]


@dataclass(frozen=True)
class Message:
    type: MessageType
    content: str
    tool_calls: tuple[ToolCall, ...] = ()
    tool_call_id: str | None = None
