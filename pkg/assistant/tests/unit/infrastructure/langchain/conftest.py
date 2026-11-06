import pytest
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from langchain.messages import AIMessage, ToolMessage


class SpyAgent:
    def __init__(self, replies: list) -> None:
        self._replies = replies
        self.received: list[dict] = []

    async def ainvoke(self, input: dict) -> dict:
        self.received.append(input)
        return {"messages": [*input["messages"], *self._replies]}


class FailingAgent:
    async def ainvoke(self, input: dict) -> dict:
        raise TimeoutError("provider unavailable")


@pytest.fixture
def messages() -> list[Message]:
    return [
        Message(type=MessageType.PATIENT, content="Hola"),
        Message(
            type=MessageType.ASSISTANT,
            content="",
            tool_calls=(ToolCall(id="call-1", name="find_sessions", arguments={"limit": 1}),),
        ),
        Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1"),
        Message(type=MessageType.ASSISTANT, content="Hola, ¿cómo estás?"),
        Message(type=MessageType.PATIENT, content="Me cuesta dormir"),
    ]


@pytest.fixture
def agent() -> SpyAgent:
    return SpyAgent(
        replies=[
            AIMessage(
                content="",
                tool_calls=[{"id": "call-2", "name": "find_notes", "args": {"topic": "sueño"}}],
            ),
            ToolMessage(content="Sin notas", tool_call_id="call-2"),
            AIMessage(content="¿Desde cuándo te pasa?"),
        ]
    )


@pytest.fixture
def failing_agent() -> FailingAgent:
    return FailingAgent()
