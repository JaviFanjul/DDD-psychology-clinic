import pytest
from assistant.application.command.activate_patient import ActivatePatientCommand
from assistant.application.command.deactivate_patient import DeactivatePatientCommand
from assistant.domain.model.patient.errors import InvalidPatientId
from assistant.domain.model.patient.patient_id import PatientId


@pytest.mark.parametrize(
    ("routing_key", "expected_command"),
    [
        ("patient.created", ActivatePatientCommand),
        ("patient.readmitted", ActivatePatientCommand),
        ("patient.discharged", DeactivatePatientCommand),
    ],
)
async def test_given_a_patient_event_when_consuming_then_it_dispatches_its_command(
    consumer, command_bus, message, patient_id, routing_key, expected_command
):
    await consumer.consume(message=message(routing_key=routing_key, patient_id=patient_id))

    assert command_bus.handled == [expected_command(id=PatientId.from_string(id=patient_id))]


async def test_given_a_malformed_patient_id_when_consuming_then_it_raises_and_dispatches_nothing(
    consumer, command_bus, message
):
    with pytest.raises(InvalidPatientId):
        await consumer.consume(message=message(routing_key="patient.created", patient_id="bad"))

    assert command_bus.handled == []
