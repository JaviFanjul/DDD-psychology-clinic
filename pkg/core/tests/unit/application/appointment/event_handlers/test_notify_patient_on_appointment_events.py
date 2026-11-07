import pytest
from core.application.appointment.event_handlers.notify_patient_on_appointment_cancelled import (
    NotifyPatientOnAppointmentCancelled,
)
from core.application.appointment.event_handlers.notify_patient_on_appointment_modality_changed import (
    NotifyPatientOnAppointmentModalityChanged,
)
from core.application.appointment.event_handlers.notify_patient_on_appointment_rescheduled import (
    NotifyPatientOnAppointmentRescheduled,
)
from core.application.appointment.event_handlers.notify_patient_on_appointment_scheduled import (
    NotifyPatientOnAppointmentScheduled,
)
from core.application.appointment.event_handlers.request_feedback_from_patient_on_appointment_completed import (
    RequestFeedbackFromPatientOnAppointmentCompleted,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.errors import AppointmentNotFound
from core.domain.model.appointment.events import (
    AppointmentCancelled,
    AppointmentCompleted,
    AppointmentModalityChanged,
    AppointmentRescheduled,
    AppointmentScheduled,
)
from core.domain.model.patient.errors import PatientNotFound

HANDLERS = [
    (NotifyPatientOnAppointmentScheduled, AppointmentScheduled, "appointment_scheduled"),
    (NotifyPatientOnAppointmentRescheduled, AppointmentRescheduled, "appointment_rescheduled"),
    (
        NotifyPatientOnAppointmentModalityChanged,
        AppointmentModalityChanged,
        "appointment_modality_changed",
    ),
    (NotifyPatientOnAppointmentCancelled, AppointmentCancelled, "appointment_cancelled"),
    (RequestFeedbackFromPatientOnAppointmentCompleted, AppointmentCompleted, "request_feedback"),
]


@pytest.mark.parametrize(("handler_type", "event_type", "notification"), HANDLERS)
async def test_given_a_known_appointment_when_handling_then_its_patient_is_notified(
    appointments,
    repository,
    notifier,
    known_appointment_id,
    known_appointment,
    known_patient,
    handler_type,
    event_type,
    notification,
):
    handler = handler_type(appointments=appointments, patients=repository, notifier=notifier)

    await handler.handle(event=event_type(appointment_id=known_appointment_id))

    assert notifier.notified == [(notification, known_patient, known_appointment)]


@pytest.mark.parametrize(("handler_type", "event_type", "notification"), HANDLERS)
async def test_given_an_unknown_appointment_when_handling_then_it_raises_and_notifies_nobody(
    appointments, repository, notifier, handler_type, event_type, notification
):
    handler = handler_type(appointments=appointments, patients=repository, notifier=notifier)

    with pytest.raises(AppointmentNotFound):
        await handler.handle(event=event_type(appointment_id=AppointmentId.generate()))

    assert notifier.notified == []


@pytest.mark.parametrize(("handler_type", "event_type", "notification"), HANDLERS)
async def test_given_an_appointment_of_an_unknown_patient_when_handling_then_it_raises(
    appointments,
    repository,
    notifier,
    orphan_appointment_id,
    handler_type,
    event_type,
    notification,
):
    handler = handler_type(appointments=appointments, patients=repository, notifier=notifier)

    with pytest.raises(PatientNotFound):
        await handler.handle(event=event_type(appointment_id=orphan_appointment_id))

    assert notifier.notified == []
