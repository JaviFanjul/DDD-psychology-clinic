import pytest
from assistant.application.command.start_conversation import StartConversationCommand
from assistant.application.command.talk_to_assistant import TalkToAssistantCommand
from assistant.application.query.get_conversation import GetConversationQuery
from assistant.domain.model.conversation.conversation_id import ConversationId
from assistant.domain.model.conversation.errors import InvalidConversationId
from assistant.domain.model.patient.errors import InvalidPatientId
from assistant.domain.model.patient.patient_id import PatientId


async def test_given_a_patient_when_starting_then_it_dispatches_the_command_with_the_returned_id(
    controller, command_bus, patient_id
):
    id = await controller.start(patient_id=patient_id)

    assert command_bus.handled == [
        StartConversationCommand(
            id=ConversationId.from_string(id=id), patient_id=PatientId.from_string(id=patient_id)
        )
    ]


async def test_given_two_starts_when_starting_then_each_gets_its_own_id(controller, patient_id):
    first_id = await controller.start(patient_id=patient_id)
    second_id = await controller.start(patient_id=patient_id)

    assert first_id != second_id


async def test_given_a_malformed_patient_id_when_starting_then_it_raises_and_dispatches_nothing(
    controller, command_bus
):
    with pytest.raises(InvalidPatientId):
        await controller.start(patient_id="not-a-uuid")

    assert command_bus.handled == []


async def test_given_a_message_when_talking_then_it_dispatches_the_command_and_returns_the_reply(
    controller, command_bus, conversation_id, patient_id
):
    reply = await controller.talk(
        id=conversation_id, patient_id=patient_id, content="Me cuesta dormir"
    )

    assert command_bus.handled == [
        TalkToAssistantCommand(
            conversation_id=ConversationId.from_string(id=conversation_id),
            patient_id=PatientId.from_string(id=patient_id),
            content="Me cuesta dormir",
        )
    ]
    assert reply == "¿Desde cuándo te pasa?"


@pytest.mark.parametrize(
    ("field", "expected_error"),
    [("id", InvalidConversationId), ("patient_id", InvalidPatientId)],
)
async def test_given_a_malformed_id_when_talking_then_it_raises_and_dispatches_nothing(
    controller, command_bus, conversation_id, patient_id, field, expected_error
):
    data = {"id": conversation_id, "patient_id": patient_id, "content": "Me cuesta dormir"}

    with pytest.raises(expected_error):
        await controller.talk(**{**data, field: "not-a-uuid"})

    assert command_bus.handled == []


async def test_given_an_id_when_getting_then_it_dispatches_the_query_and_returns_its_result(
    controller, query_bus, conversation_dto
):
    conversation = await controller.get(id=conversation_dto.id)

    assert query_bus.handled == [
        GetConversationQuery(id=ConversationId.from_string(id=conversation_dto.id))
    ]
    assert conversation == conversation_dto


async def test_given_a_malformed_id_when_getting_then_it_raises_and_dispatches_nothing(
    controller, query_bus
):
    with pytest.raises(InvalidConversationId):
        await controller.get(id="not-a-uuid")

    assert query_bus.handled == []
