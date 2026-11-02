import pytest
from core.application.command.readmit_patient import ReadmitPatientCommand
from core.domain.model.patient.errors import PatientAlreadyActive, PatientNotFound
from core.domain.model.patient.events import PatientReadmitted
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_status import PatientStatus


async def test_given_a_discharged_patient_when_handling_then_it_is_saved_active(
    readmit_handler, repository, discharged_patient
):
    await readmit_handler.handle(command=ReadmitPatientCommand(id=discharged_patient.id))

    [patient] = repository.saved
    assert patient.id == discharged_patient.id
    assert patient.status is PatientStatus.ACTIVE


async def test_given_a_discharged_patient_when_handling_then_patient_readmitted_is_published(
    readmit_handler, event_bus, discharged_patient
):
    await readmit_handler.handle(command=ReadmitPatientCommand(id=discharged_patient.id))

    [event] = event_bus.published
    assert isinstance(event, PatientReadmitted)
    assert event.patient_id == discharged_patient.id


async def test_given_an_unknown_id_when_handling_then_it_raises_and_saves_and_publishes_nothing(
    readmit_handler, repository, event_bus
):
    with pytest.raises(PatientNotFound):
        await readmit_handler.handle(command=ReadmitPatientCommand(id=PatientId.generate()))

    assert repository.saved == []
    assert event_bus.published == []


async def test_given_an_active_patient_when_handling_then_it_raises_and_saves_nothing(
    readmit_handler, repository, event_bus, active_patient
):
    with pytest.raises(PatientAlreadyActive):
        await readmit_handler.handle(command=ReadmitPatientCommand(id=active_patient.id))

    assert repository.saved == []
    assert event_bus.published == []
