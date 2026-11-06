import pytest
from assistant.application.command.deactivate_patient import DeactivatePatientCommand
from assistant.domain.model.patient.errors import PatientNotFound


async def test_given_an_unknown_patient_when_handling_then_it_raises_and_saves_nothing(
    deactivate_handler, repository, unknown_patient_id
):
    with pytest.raises(PatientNotFound):
        await deactivate_handler.handle(command=DeactivatePatientCommand(id=unknown_patient_id))

    assert repository.saved == []


@pytest.mark.parametrize("stored_patient", ["active_patient", "inactive_patient"])
async def test_given_a_known_patient_when_handling_then_it_is_saved_inactive(
    deactivate_handler, repository, stored_patient, request
):
    patient_id = request.getfixturevalue(stored_patient).id

    await deactivate_handler.handle(command=DeactivatePatientCommand(id=patient_id))

    [patient] = repository.saved
    assert patient.id == patient_id
    assert not patient.is_active
