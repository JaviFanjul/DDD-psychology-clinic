import pytest
from core.application.command.create_patient import CreatePatientCommand
from core.application.query.get_patient import GetPatientQuery
from core.domain.model.patient.errors import (
    InvalidPatientAddress,
    InvalidPatientEmail,
    InvalidPatientId,
    InvalidPatientName,
)
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName


def test_given_valid_data_when_creating_then_it_dispatches_the_command_with_the_returned_id(
    controller, command_bus, create_data
):
    id = controller.create(**create_data)

    assert command_bus.handled == [
        CreatePatientCommand(
            id=PatientId.from_string(id=id),
            email=PatientEmail(value="ana@gmail.com"),
            name=PatientName(first_name="Ana", last_names="García López"),
            address=PatientAddress(
                street="Calle Mayor 3, 2º B",
                postal_code="08001",
                city="Barcelona",
                province="Barcelona",
            ),
        )
    ]


def test_given_two_creations_when_creating_then_each_gets_its_own_id(controller, create_data):
    first_id = controller.create(**create_data)
    second_id = controller.create(**create_data)

    assert first_id != second_id


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_error"),
    [
        ("email", "not-an-email", InvalidPatientEmail),
        ("first_name", "   ", InvalidPatientName),
        ("postal_code", "0800", InvalidPatientAddress),
    ],
)
def test_given_an_invalid_field_when_creating_then_it_raises_and_dispatches_nothing(
    controller, command_bus, create_data, field, invalid_value, expected_error
):
    with pytest.raises(expected_error):
        controller.create(**{**create_data, field: invalid_value})

    assert command_bus.handled == []


def test_given_an_id_when_getting_then_it_dispatches_the_query_and_returns_its_result(
    controller, query_bus, patient_dto
):
    patient = controller.get(id=patient_dto.id)

    assert query_bus.handled == [GetPatientQuery(id=PatientId.from_string(id=patient_dto.id))]
    assert patient == patient_dto


def test_given_a_malformed_id_when_getting_then_it_raises_and_dispatches_nothing(
    controller, query_bus
):
    with pytest.raises(InvalidPatientId):
        controller.get(id="not-a-uuid")

    assert query_bus.handled == []
