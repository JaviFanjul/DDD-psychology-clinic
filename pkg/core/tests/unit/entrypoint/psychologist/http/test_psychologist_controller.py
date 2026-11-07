import pytest
from core.application.psychologist.command.create_psychologist import CreatePsychologistCommand
from core.application.psychologist.query.get_psychologist import GetPsychologistQuery
from core.domain.model.psychologist.errors import (
    InvalidPsychologistEmail,
    InvalidPsychologistId,
    InvalidPsychologistLicenseNumber,
    InvalidPsychologistName,
    InvalidPsychologistPhone,
)
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone


async def test_given_valid_data_when_creating_then_it_dispatches_the_command_with_the_returned_id(
    controller, command_bus, create_data
):
    id = await controller.create(**create_data)

    assert command_bus.handled == [
        CreatePsychologistCommand(
            id=PsychologistId.from_string(id=id),
            email=PsychologistEmail(value="laura@clinica.es"),
            name=PsychologistName(first_name="Laura", last_names="Martín Ruiz"),
            phone=PsychologistPhone(prefix="+34", number="687654321"),
            license_number=PsychologistLicenseNumber(value="M-12345"),
        )
    ]


async def test_given_two_creations_when_creating_then_each_gets_its_own_id(controller, create_data):
    first_id = await controller.create(**create_data)
    second_id = await controller.create(**create_data)

    assert first_id != second_id


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_error"),
    [
        ("email", "not-an-email", InvalidPsychologistEmail),
        ("first_name", "   ", InvalidPsychologistName),
        ("phone_number", "123", InvalidPsychologistPhone),
        ("license_number", "M-123", InvalidPsychologistLicenseNumber),
    ],
)
async def test_given_an_invalid_field_when_creating_then_it_raises_and_dispatches_nothing(
    controller, command_bus, create_data, field, invalid_value, expected_error
):
    with pytest.raises(expected_error):
        await controller.create(**{**create_data, field: invalid_value})

    assert command_bus.handled == []


async def test_given_an_id_when_getting_then_it_dispatches_the_query_and_returns_its_result(
    controller, query_bus, psychologist_dto
):
    psychologist = await controller.get(id=psychologist_dto.id)

    assert query_bus.handled == [
        GetPsychologistQuery(id=PsychologistId.from_string(id=psychologist_dto.id))
    ]
    assert psychologist == psychologist_dto


async def test_given_a_malformed_id_when_getting_then_it_raises_and_dispatches_nothing(
    controller, query_bus
):
    with pytest.raises(InvalidPsychologistId):
        await controller.get(id="not-a-uuid")

    assert query_bus.handled == []
