import pytest
from core.application.query.get_appointment import GetAppointmentQuery
from core.domain.model.appointment.appointment_id import AppointmentId
from core.domain.model.appointment.errors import AppointmentNotFound


async def test_given_a_known_id_when_handling_then_it_returns_the_appointment(
    appointment_handler, known_id, known_appointment
):
    appointment = await appointment_handler.handle(
        query=GetAppointmentQuery(id=AppointmentId.from_string(id=known_id))
    )

    assert appointment == known_appointment


async def test_given_an_id_without_an_appointment_when_handling_then_it_raises_not_found(
    appointment_handler,
):
    with pytest.raises(AppointmentNotFound):
        await appointment_handler.handle(query=GetAppointmentQuery(id=AppointmentId.generate()))
