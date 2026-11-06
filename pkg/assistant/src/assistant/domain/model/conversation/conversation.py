from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import ConversationNotOwned
from assistant.domain.model.conversation.message import Message, MessageType
from assistant.domain.model.patient.patient_id import PatientId


class Conversation:
    def __init__(self, id: ConversationId, patient_id: PatientId, messages: list[Message]) -> None:
        self._id = id
        self._patient_id = patient_id
        self._messages = list(messages)

    @property
    def id(self) -> ConversationId:
        return self._id

    @property
    def patient_id(self) -> PatientId:
        return self._patient_id

    @property
    def messages(self) -> list[Message]:
        return list(self._messages)

    @classmethod
    def start(cls, id: ConversationId, patient_id: PatientId) -> Conversation:
        conversation: Conversation = cls(id=id, patient_id=patient_id, messages=[])
        return conversation

    def patient_writes(self, patient_id: PatientId, content: str) -> None:
        if patient_id != self._patient_id:
            raise ConversationNotOwned(id=str(self._id), patient_id=str(patient_id))
        self._messages.append(Message(type=MessageType.PATIENT, content=content))

    def assistant_replies(self, messages: list[Message]) -> None:
        self._messages.extend(messages)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Conversation) and other._id == self._id

    def __hash__(self) -> int:
        return hash(self._id)
