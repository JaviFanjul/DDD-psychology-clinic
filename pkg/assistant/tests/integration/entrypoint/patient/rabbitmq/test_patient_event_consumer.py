from assistant.application.command.activate_patient import ActivatePatientCommand
from assistant.application.command.deactivate_patient import DeactivatePatientCommand
from assistant.domain.model.patient.patient_id import PatientId


async def test_given_patient_events_from_core_when_consuming_then_their_commands_are_dispatched(
    consume, publish, wait_until, patient_id, command_bus
):
    await consume(command_bus=command_bus)

    for routing_key in ("patient.created", "patient.discharged", "patient.readmitted"):
        await publish(routing_key=routing_key, patient_id=patient_id)
    await wait_until(condition=lambda: len(command_bus.handled) == 3)

    id = PatientId.from_string(id=patient_id)
    assert command_bus.handled == [
        ActivatePatientCommand(id=id),
        DeactivatePatientCommand(id=id),
        ActivatePatientCommand(id=id),
    ]


async def test_given_a_command_that_fails_when_consuming_then_the_event_is_delivered_again(
    consume, publish, wait_until, patient_id, failing_once_command_bus
):
    command_bus = failing_once_command_bus
    await consume(command_bus=command_bus)

    await publish(routing_key="patient.discharged", patient_id=patient_id)
    await wait_until(condition=lambda: len(command_bus.handled) == 2)

    id = PatientId.from_string(id=patient_id)
    assert command_bus.handled == [DeactivatePatientCommand(id=id), DeactivatePatientCommand(id=id)]
