import pytest
from core.application.command.create_patient import CreatePatientCommand
from core.application.command.discharge_patient import DischargePatientCommand
from core.application.query.get_patient import GetPatientQuery
from core.domain.model.patient.errors import (
    InvalidPatientAddress,
    InvalidPatientEmail,
    InvalidPatientId,
    InvalidPatientName,
    InvalidPatientPhone,
)
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone


async def test_given_valid_data_when_creating_then_it_dispatches_the_command_with_the_returned_id(
    controller, command_bus, create_data
):
    id = await controller.create(**create_data)

    assert command_bus.handled == [
        CreatePatientCommand(
            id=PatientId.from_string(id=id),
            email=PatientEmail(value="ana@gmail.com"),
            name=PatientName(first_name="Ana", last_names="García López"),
            phone=PatientPhone(prefix="+34", number="612345678"),
            address=PatientAddress(
                street="Calle Mayor 3, 2º B",
                postal_code="08001",
                city="Barcelona",
                province="Barcelona",
            ),
        )
    ]


async def test_given_two_creations_when_creating_then_each_gets_its_own_id(controller, create_data):
    first_id = await controller.create(**create_data)
    second_id = await controller.create(**create_data)

    assert first_id != second_id


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_error"),
    [
        ("email", "not-an-email", InvalidPatientEmail),
        ("first_name", "   ", InvalidPatientName),
        ("phone_number", "123", InvalidPatientPhone),
        ("postal_code", "0800", InvalidPatientAddress),
    ],
)
async def test_given_an_invalid_field_when_creating_then_it_raises_and_dispatches_nothing(
    controller, command_bus, create_data, field, invalid_value, expected_error
):
    with pytest.raises(expected_error):
        await controller.create(**{**create_data, field: invalid_value})

    assert command_bus.handled == []


async def test_given_an_id_when_getting_then_it_dispatches_the_query_and_returns_its_result(
    controller, query_bus, patient_dto
):
    patient = await controller.get(id=patient_dto.id)

    assert query_bus.handled == [GetPatientQuery(id=PatientId.from_string(id=patient_dto.id))]
    assert patient == patient_dto


async def test_given_a_malformed_id_when_getting_then_it_raises_and_dispatches_nothing(
    controller, query_bus
):
    with pytest.raises(InvalidPatientId):
        await controller.get(id="not-a-uuid")

    assert query_bus.handled == []


async def test_given_an_id_when_discharging_then_it_dispatches_the_command(
    controller, command_bus, patient_dto
):
    await controller.discharge(id=patient_dto.id)

    assert command_bus.handled == [
        DischargePatientCommand(id=PatientId.from_string(id=patient_dto.id))
    ]


async def test_given_a_malformed_id_when_discharging_then_it_raises_and_dispatches_nothing(
    controller, command_bus
):
    with pytest.raises(InvalidPatientId):
        await controller.discharge(id="not-a-uuid")

    assert command_bus.handled == []
