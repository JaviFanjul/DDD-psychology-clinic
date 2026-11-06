from assistant.domain.domain_error import DomainError


class InvalidConversationId(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"{value!r} is not a valid UUID")


class ConversationNotFound(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Conversation {id!r} was not found")


class ConversationNotOwned(DomainError):
    def __init__(self, id: str, patient_id: str) -> None:
        super().__init__(f"Conversation {id!r} does not belong to patient {patient_id!r}")


class ConversationNotSaved(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Conversation {id!r} could not be saved")


class ConversationNotLoaded(DomainError):
    def __init__(self, id: str) -> None:
        super().__init__(f"Conversation {id!r} could not be loaded")


class AssistantNotAnswered(DomainError):
    def __init__(self) -> None:
        super().__init__("The assistant could not answer")
