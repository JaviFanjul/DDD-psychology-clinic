import pytest
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.events import PatientReadmitted
from core.domain.model.patient.patient_id import PatientId


async def test_given_a_known_patient_when_it_is_readmitted_then_they_are_welcomed_back(
    welcome_back_handler, notifier, known_id, known_patient
):
    await welcome_back_handler.handle(event=PatientReadmitted(patient_id=known_id))

    assert notifier.welcomed_back == [known_patient]


async def test_given_an_unknown_patient_when_it_is_readmitted_then_nobody_is_welcomed_back(
    welcome_back_handler, notifier
):
    with pytest.raises(PatientNotFound):
        await welcome_back_handler.handle(event=PatientReadmitted(patient_id=PatientId.generate()))

    assert notifier.welcomed_back == []
