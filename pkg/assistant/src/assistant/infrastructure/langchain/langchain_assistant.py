from typing import Any

from assistant.domain.model.conversation.assistant import Assistant
from assistant.domain.model.conversation.errors import AssistantNotAnswered
from assistant.domain.model.conversation.message import Message
from assistant.infrastructure.langchain.langchain_message_mapper import LangChainMessageMapper
from langgraph.graph.state import CompiledStateGraph


class LangChainAssistant(Assistant):
    def __init__(self, agent: CompiledStateGraph[Any, Any, Any, Any]) -> None:
        self._agent = agent

    async def ask(self, messages: list[Message]) -> list[Message]:
        try:
            result = await self._agent.ainvoke(
                {
                    "messages": [
                        LangChainMessageMapper.to_langchain(message=message) for message in messages
                    ]
                }
            )
        except Exception as error:
            raise AssistantNotAnswered() from error
        replies: list[Message] = [
            LangChainMessageMapper.to_domain(message=message)
            for message in result["messages"][len(messages) :]
        ]
        return replies
