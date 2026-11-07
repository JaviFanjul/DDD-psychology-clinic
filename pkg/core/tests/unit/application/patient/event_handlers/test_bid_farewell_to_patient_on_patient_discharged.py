import pytest
from core.domain.model.patient.errors import PatientNotFound
from core.domain.model.patient.events import PatientDischarged
from core.domain.model.patient.patient_id import PatientId


async def test_given_a_known_patient_when_it_is_discharged_then_they_are_bid_farewell(
    farewell_handler, notifier, known_id, known_patient
):
    await farewell_handler.handle(event=PatientDischarged(patient_id=known_id))

    assert notifier.farewelled == [known_patient]


async def test_given_an_unknown_patient_when_it_is_discharged_then_nobody_is_bid_farewell(farewell_handler, notifier):
    with pytest.raises(PatientNotFound):
        await farewell_handler.handle(event=PatientDischarged(patient_id=PatientId.generate()))

    assert notifier.farewelled == []
