import pytest
from assistant.domain.model.conversation.errors import AssistantNotAnswered
from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from assistant.infrastructure.langchain.langchain_assistant import LangChainAssistant
from langchain.messages import AIMessage, HumanMessage, ToolMessage


async def test_given_messages_when_asking_then_it_returns_only_the_messages_of_this_turn(
    agent, messages
):
    assistant = LangChainAssistant(agent=agent)

    replies = await assistant.ask(messages=messages)

    assert replies == [
        Message(
            type=MessageType.ASSISTANT,
            content="",
            tool_calls=(ToolCall(id="call-2", name="find_notes", arguments={"topic": "sueño"}),),
        ),
        Message(type=MessageType.TOOL, content="Sin notas", tool_call_id="call-2"),
        Message(type=MessageType.ASSISTANT, content="¿Desde cuándo te pasa?"),
    ]


async def test_given_messages_when_asking_then_the_agent_receives_the_whole_history_in_order(
    agent, messages
):
    assistant = LangChainAssistant(agent=agent)

    await assistant.ask(messages=messages)

    [received] = agent.received
    assert [type(message) for message in received["messages"]] == [
        HumanMessage,
        AIMessage,
        ToolMessage,
        AIMessage,
        HumanMessage,
    ]


async def test_given_a_failing_agent_when_asking_then_it_raises_assistant_not_answered(
    failing_agent, messages
):
    assistant = LangChainAssistant(agent=failing_agent)

    with pytest.raises(AssistantNotAnswered) as raised:
        await assistant.ask(messages=messages)

    assert isinstance(raised.value.__cause__, TimeoutError)
