from assistant.domain.model.conversation.message import Message, MessageType, ToolCall
from langchain.messages import AIMessage, AnyMessage, HumanMessage, ToolMessage


class LangChainMessageMapper:
    @staticmethod
    def to_langchain(message: Message) -> AnyMessage:
        if message.type is MessageType.PATIENT:
            return HumanMessage(content=message.content)
        if message.type is MessageType.TOOL:
            return ToolMessage(content=message.content, tool_call_id=message.tool_call_id)
        return AIMessage(
            content=message.content,
            tool_calls=[
                {"id": tool_call.id, "name": tool_call.name, "args": tool_call.arguments}
                for tool_call in message.tool_calls
            ],
        )

    @staticmethod
    def to_domain(message: AnyMessage) -> Message:
        if isinstance(message, ToolMessage):
            return Message(
                type=MessageType.TOOL, content=message.text, tool_call_id=message.tool_call_id
            )
        if isinstance(message, AIMessage):
            return Message(
                type=MessageType.ASSISTANT,
                content=message.text,
                tool_calls=tuple(
                    ToolCall(
                        id=tool_call["id"] or "",
                        name=tool_call["name"],
                        arguments=tool_call["args"],
                    )
                    for tool_call in message.tool_calls
                ),
            )
        return Message(type=MessageType.PATIENT, content=message.text)
