import pytest
from core.application.event_handlers.notify_psychologist_on_appointment_cancelled import (
    NotifyPsychologistOnAppointmentCancelled,
)
from core.application.event_handlers.notify_psychologist_on_appointment_modality_changed import (
    NotifyPsychologistOnAppointmentModalityChanged,
)
from core.application.event_handlers.notify_psychologist_on_appointment_rescheduled import (
    NotifyPsychologistOnAppointmentRescheduled,
)
from core.application.event_handlers.notify_psychologist_on_appointment_scheduled import (
    NotifyPsychologistOnAppointmentScheduled,
)
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.errors import AppointmentNotFound
from core.domain.model.appointment.events import (
    AppointmentCancelled,
    AppointmentModalityChanged,
    AppointmentRescheduled,
    AppointmentScheduled,
)
from core.domain.model.psychologist.errors import PsychologistNotFound

HANDLERS = [
    (NotifyPsychologistOnAppointmentScheduled, AppointmentScheduled, "appointment_scheduled"),
    (
        NotifyPsychologistOnAppointmentRescheduled,
        AppointmentRescheduled,
        "appointment_rescheduled",
    ),
    (
        NotifyPsychologistOnAppointmentModalityChanged,
        AppointmentModalityChanged,
        "appointment_modality_changed",
    ),
    (NotifyPsychologistOnAppointmentCancelled, AppointmentCancelled, "appointment_cancelled"),
]


@pytest.mark.parametrize(("handler_type", "event_type", "notification"), HANDLERS)
async def test_given_a_known_appointment_when_handling_then_its_psychologist_is_notified(
    appointments,
    psychologists,
    psychologist_notifier,
    known_appointment_id,
    known_appointment,
    known_psychologist,
    handler_type,
    event_type,
    notification,
):
    handler = handler_type(
        appointments=appointments, psychologists=psychologists, notifier=psychologist_notifier
    )

    await handler.handle(event=event_type(appointment_id=known_appointment_id))

    assert psychologist_notifier.notified == [(notification, known_psychologist, known_appointment)]


@pytest.mark.parametrize(("handler_type", "event_type", "notification"), HANDLERS)
async def test_given_an_unknown_appointment_when_handling_then_it_raises_and_notifies_nobody(
    appointments, psychologists, psychologist_notifier, handler_type, event_type, notification
):
    handler = handler_type(
        appointments=appointments, psychologists=psychologists, notifier=psychologist_notifier
    )

    with pytest.raises(AppointmentNotFound):
        await handler.handle(event=event_type(appointment_id=AppointmentId.generate()))

    assert psychologist_notifier.notified == []


@pytest.mark.parametrize(("handler_type", "event_type", "notification"), HANDLERS)
async def test_given_an_appointment_of_an_unknown_psychologist_when_handling_then_it_raises(
    appointments,
    psychologists,
    psychologist_notifier,
    orphan_appointment_id,
    handler_type,
    event_type,
    notification,
):
    handler = handler_type(
        appointments=appointments, psychologists=psychologists, notifier=psychologist_notifier
    )

    with pytest.raises(PsychologistNotFound):
        await handler.handle(event=event_type(appointment_id=orphan_appointment_id))

    assert psychologist_notifier.notified == []
