import pytest
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.events import PatientCreated
from core.domain.model.patient.patient_id import PatientId


async def test_given_a_known_patient_when_it_is_created_then_they_are_welcomed(
    handler, notifier, known_id, known_patient
):
    await handler.handle(event=PatientCreated(patient_id=known_id))

    assert notifier.welcomed == [known_patient]


async def test_given_an_unknown_patient_when_it_is_created_then_nobody_is_welcomed(
    handler, notifier
):
    with pytest.raises(PatientNotFound):
        await handler.handle(event=PatientCreated(patient_id=PatientId.generate()))

    assert notifier.welcomed == []
