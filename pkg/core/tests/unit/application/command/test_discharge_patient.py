import pytest
from core.application.command.discharge_patient import DischargePatientCommand
from core.domain.model.patient.errors import PatientAlreadyDischarged, PatientNotFound
from core.domain.model.patient.events import PatientDischarged
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_status import PatientStatus


async def test_given_an_active_patient_when_handling_then_it_is_saved_discharged(
    discharge_handler, repository, active_patient
):
    await discharge_handler.handle(command=DischargePatientCommand(id=active_patient.id))

    [patient] = repository.saved
    assert patient.id == active_patient.id
    assert patient.status is PatientStatus.DISCHARGED


async def test_given_an_active_patient_when_handling_then_patient_discharged_is_published(
    discharge_handler, event_bus, active_patient
):
    await discharge_handler.handle(command=DischargePatientCommand(id=active_patient.id))

    [event] = event_bus.published
    assert isinstance(event, PatientDischarged)
    assert event.patient_id == active_patient.id


async def test_given_an_unknown_id_when_handling_then_it_raises_and_saves_and_publishes_nothing(
    discharge_handler, repository, event_bus
):
    with pytest.raises(PatientNotFound):
        await discharge_handler.handle(command=DischargePatientCommand(id=PatientId.generate()))

    assert repository.saved == []
    assert event_bus.published == []


async def test_given_a_discharged_patient_when_handling_then_it_raises_and_saves_nothing(
    discharge_handler, repository, event_bus, discharged_patient
):
    with pytest.raises(PatientAlreadyDischarged):
        await discharge_handler.handle(command=DischargePatientCommand(id=discharged_patient.id))

    assert repository.saved == []
    assert event_bus.published == []
