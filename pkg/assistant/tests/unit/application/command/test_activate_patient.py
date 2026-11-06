import pytest
from assistant.application.command.activate_patient import ActivatePatientCommand


async def test_given_an_unknown_patient_when_handling_then_it_is_saved_active(
    activate_handler, repository, unknown_patient_id
):
    await activate_handler.handle(command=ActivatePatientCommand(id=unknown_patient_id))

    [patient] = repository.saved
    assert patient.id == unknown_patient_id
    assert patient.is_active


@pytest.mark.parametrize("stored_patient", ["active_patient", "inactive_patient"])
async def test_given_a_known_patient_when_handling_then_it_is_saved_active(
    activate_handler, repository, stored_patient, request
):
    patient_id = request.getfixturevalue(stored_patient).id

    await activate_handler.handle(command=ActivatePatientCommand(id=patient_id))

    [patient] = repository.saved
    assert patient.id == patient_id
    assert patient.is_active
