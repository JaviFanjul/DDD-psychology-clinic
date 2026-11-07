import pytest
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from assistant.infrastructure.langchain.langchain_message_mapper import LangChainMessageMapper
from langchain.messages import AIMessage, HumanMessage, ToolMessage

TOOL_CALL = ToolCall(id="call-1", name="find_sessions", arguments={"limit": 1})


@pytest.mark.parametrize(
    ("message", "expected_type"),
    [
        (Message(type=MessageType.PATIENT, content="Hola"), HumanMessage),
        (Message(type=MessageType.ASSISTANT, content="Hola, ¿cómo estás?"), AIMessage),
        (
            Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1"),
            ToolMessage,
        ),
    ],
)
def test_given_a_message_when_mapping_to_langchain_then_it_gets_its_langchain_type_and_content(message, expected_type):
    mapped = LangChainMessageMapper.to_langchain(message=message)

    assert type(mapped) is expected_type
    assert mapped.content == message.content


def test_given_an_assistant_message_with_tool_calls_when_mapping_to_langchain_then_it_keeps_them():
    message = Message(type=MessageType.ASSISTANT, content="", tool_calls=(TOOL_CALL,))

    mapped = LangChainMessageMapper.to_langchain(message=message)

    assert [(call["id"], call["name"], call["args"]) for call in mapped.tool_calls] == [
        ("call-1", "find_sessions", {"limit": 1})
    ]


def test_given_a_tool_message_when_mapping_to_langchain_then_it_keeps_its_tool_call_id():
    message = Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1")

    mapped = LangChainMessageMapper.to_langchain(message=message)

    assert mapped.tool_call_id == "call-1"


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        (HumanMessage(content="Hola"), Message(type=MessageType.PATIENT, content="Hola")),
        (
            AIMessage(content="¿Desde cuándo?"),
            Message(type=MessageType.ASSISTANT, content="¿Desde cuándo?"),
        ),
        (
            AIMessage(
                content="",
                tool_calls=[{"id": "call-1", "name": "find_sessions", "args": {"limit": 1}}],
            ),
            Message(type=MessageType.ASSISTANT, content="", tool_calls=(TOOL_CALL,)),
        ),
        (
            ToolMessage(content="Última sesión: lunes", tool_call_id="call-1"),
            Message(type=MessageType.TOOL, content="Última sesión: lunes", tool_call_id="call-1"),
        ),
    ],
)
def test_given_a_langchain_message_when_mapping_to_domain_then_it_rebuilds_the_message(message, expected):
    mapped = LangChainMessageMapper.to_domain(message=message)

    assert mapped == expected
