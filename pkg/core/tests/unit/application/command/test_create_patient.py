from core.application.command.create_patient import CreatePatientCommand
from core.domain.model.patient.events import PatientCreated
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId


def test_given_a_command_when_handling_then_the_patient_is_saved(handler, repository):
    id = PatientId.generate()
    email = PatientEmail("ana@gmail.com")

    handler.handle(CreatePatientCommand(id=id, email=email))

    [patient] = repository.saved
    assert patient.id == id
    assert patient.email == email


def test_given_a_command_when_handling_then_patient_created_is_published(handler, event_bus):
    id = PatientId.generate()

    handler.handle(CreatePatientCommand(id=id, email=PatientEmail("ana@gmail.com")))

    [event] = event_bus.published
    assert isinstance(event, PatientCreated)
    assert event.patient_id == id
