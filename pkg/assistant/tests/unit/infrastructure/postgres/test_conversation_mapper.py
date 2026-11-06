from assistant.domain.model.conversation.conversation_query_repository import (
    ConversationDto,
    MessageDto,
)
from assistant.infrastructure.postgres.conversation_mapper import ConversationMapper


def test_given_a_conversation_when_mapping_to_model_then_it_flattens_its_messages(
    conversation, conversation_model
):
    mapped = ConversationMapper.to_model(conversation=conversation)

    assert (mapped.id, mapped.patient_id, mapped.messages) == (
        conversation_model.id,
        conversation_model.patient_id,
        conversation_model.messages,
    )


def test_given_a_model_when_mapping_to_entity_then_it_rebuilds_the_conversation(
    conversation_model, conversation
):
    mapped = ConversationMapper.to_entity(model=conversation_model)

    assert mapped.id == conversation.id
    assert mapped.patient_id == conversation.patient_id
    assert mapped.messages == conversation.messages


def test_given_a_model_when_mapping_to_dto_then_it_keeps_only_what_the_patient_sees(
    conversation_model,
):
    mapped = ConversationMapper.to_dto(model=conversation_model)

    assert mapped == ConversationDto(
        id="12345678-1234-4678-9234-567812345678",
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        messages=[
            MessageDto(type="patient", content="Me cuesta dormir"),
            MessageDto(type="assistant", content="¿Desde cuándo?"),
        ],
    )
