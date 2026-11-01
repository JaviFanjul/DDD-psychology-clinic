import pytest
from core.application.command.register_patient import RegisterPatientCommand
from core.application.query.get_patient import GetPatientQuery
from core.domain.model.patient.errors import InvalidPatientEmail, InvalidPatientId
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId


def test_given_an_email_when_registering_then_it_dispatches_the_command_with_the_returned_id(
    controller, command_bus
):
    id = controller.register("ana@gmail.com")

    assert command_bus.handled == [
        RegisterPatientCommand(id=PatientId.from_string(id), email=PatientEmail("ana@gmail.com"))
    ]


def test_given_two_registrations_when_registering_then_each_gets_its_own_id(controller):
    first_id = controller.register("ana@gmail.com")
    second_id = controller.register("ana@gmail.com")

    assert first_id != second_id


def test_given_an_invalid_email_when_registering_then_it_raises_and_dispatches_nothing(
    controller, command_bus
):
    with pytest.raises(InvalidPatientEmail):
        controller.register("not-an-email")

    assert command_bus.handled == []


def test_given_an_id_when_getting_then_it_dispatches_the_query_and_returns_its_result(
    controller, query_bus, patient_dto
):
    patient = controller.get(patient_dto.id)

    assert query_bus.handled == [GetPatientQuery(id=PatientId.from_string(patient_dto.id))]
    assert patient == patient_dto


def test_given_a_malformed_id_when_getting_then_it_raises_and_dispatches_nothing(
    controller, query_bus
):
    with pytest.raises(InvalidPatientId):
        controller.get("not-a-uuid")

    assert query_bus.handled == []
