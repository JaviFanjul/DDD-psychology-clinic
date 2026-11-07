import pytest
from core.domain.model.patient.errors import InvalidPatientId
from core.domain.model.patient.events import PatientCreated, PatientDischarged, PatientReadmitted
from core.domain.model.patient.patient_id import PatientId


@pytest.mark.parametrize(
    ("routing_key", "expected_event"),
    [
        ("patient.created", PatientCreated),
        ("patient.discharged", PatientDischarged),
        ("patient.readmitted", PatientReadmitted),
    ],
)
async def test_given_a_patient_event_when_consuming_then_its_handler_receives_it(
    consumer, handler, message, patient_id, created_at, routing_key, expected_event
):
    await consumer.consume(message=message(routing_key=routing_key, patient_id=patient_id))

    assert handler.handled == [expected_event(patient_id=PatientId.from_string(id=patient_id), created_at=created_at)]


async def test_given_a_malformed_patient_id_when_consuming_then_it_raises_and_handles_nothing(
    consumer, handler, message
):
    with pytest.raises(InvalidPatientId):
        await consumer.consume(message=message(routing_key="patient.created", patient_id="bad"))

    assert handler.handled == []
