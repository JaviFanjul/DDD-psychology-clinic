import json

import pytest
from core.domain.model.patient.events import (
    PatientCreated,
    PatientDischarged,
    PatientReadmitted,
)
from core.domain.model.psychologist.events import PsychologistCreated
from core.infrastructure.rabbitmq.rabbitmq_event_serializer import RabbitMqEventSerializer


@pytest.mark.parametrize(
    ("event_type", "expected_routing_key"),
    [
        (PatientCreated, "patient.created"),
        (PatientDischarged, "patient.discharged"),
        (PatientReadmitted, "patient.readmitted"),
    ],
)
def test_given_a_patient_event_when_serializing_it_then_it_returns_its_routing_key_and_body(
    patient_id, created_at, event_type, expected_routing_key
):
    event = event_type(patient_id=patient_id, created_at=created_at)

    routing_key, body = RabbitMqEventSerializer.to_message(event=event)

    assert routing_key == expected_routing_key
    assert json.loads(body) == {
        "patient_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "created_at": "2026-11-02T10:30:00+00:00",
    }


@pytest.mark.parametrize("event_type", [PatientCreated, PatientDischarged, PatientReadmitted])
def test_given_a_serialized_patient_event_when_deserializing_it_then_it_returns_the_same_event(
    patient_id, created_at, event_type
):
    event = event_type(patient_id=patient_id, created_at=created_at)
    routing_key, body = RabbitMqEventSerializer.to_message(event=event)

    deserialized = RabbitMqEventSerializer.from_message(routing_key=routing_key, body=body)

    assert deserialized == event


def test_given_psychologist_created_when_serializing_it_then_it_returns_its_routing_key_and_body(
    psychologist_id, created_at
):
    event = PsychologistCreated(psychologist_id=psychologist_id, created_at=created_at)

    routing_key, body = RabbitMqEventSerializer.to_message(event=event)

    assert routing_key == "psychologist.created"
    assert json.loads(body) == {
        "psychologist_id": "0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        "created_at": "2026-11-02T10:30:00+00:00",
    }


def test_given_a_serialized_psychologist_created_when_deserializing_it_then_it_is_the_same_event(
    psychologist_id, created_at
):
    event = PsychologistCreated(psychologist_id=psychologist_id, created_at=created_at)
    routing_key, body = RabbitMqEventSerializer.to_message(event=event)

    deserialized = RabbitMqEventSerializer.from_message(routing_key=routing_key, body=body)

    assert deserialized == event


def test_given_an_unknown_event_when_serializing_it_then_it_raises(unknown_event):
    with pytest.raises(TypeError):
        RabbitMqEventSerializer.to_message(event=unknown_event)
