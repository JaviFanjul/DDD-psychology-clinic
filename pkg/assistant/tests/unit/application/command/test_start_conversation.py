import pytest
from assistant.application.command.start_conversation import StartConversationCommand
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.patient.errors import PatientNotActive, PatientNotFound


async def test_given_an_active_patient_when_handling_then_the_conversation_is_saved(
    start_conversation_handler, conversations, active_patient
):
    id = ConversationId.generate()

    await start_conversation_handler.handle(command=StartConversationCommand(id=id, patient_id=active_patient.id))

    [conversation] = conversations.saved
    assert conversation.id == id
    assert conversation.patient_id == active_patient.id


async def test_given_an_unknown_patient_when_handling_then_it_raises_and_saves_nothing(
    start_conversation_handler, conversations, unknown_patient_id
):
    with pytest.raises(PatientNotFound):
        await start_conversation_handler.handle(
            command=StartConversationCommand(id=ConversationId.generate(), patient_id=unknown_patient_id)
        )

    assert conversations.saved == []


async def test_given_an_inactive_patient_when_handling_then_it_raises_and_saves_nothing(
    start_conversation_handler, conversations, inactive_patient
):
    with pytest.raises(PatientNotActive):
        await start_conversation_handler.handle(
            command=StartConversationCommand(id=ConversationId.generate(), patient_id=inactive_patient.id)
        )

    assert conversations.saved == []
