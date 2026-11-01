from core.application.command.register_patient import RegisterPatientCommand
from core.domain.model.patient.events import PatientRegistered
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId


def test_given_a_command_when_handling_then_the_patient_is_saved(handler, repository):
    id = PatientId.generate()
    email = PatientEmail("ana@gmail.com")

    handler.handle(RegisterPatientCommand(id=id, email=email))

    [patient] = repository.saved
    assert patient.id == id
    assert patient.email == email


def test_given_a_command_when_handling_then_patient_registered_is_published(handler, event_bus):
    id = PatientId.generate()

    handler.handle(RegisterPatientCommand(id=id, email=PatientEmail("ana@gmail.com")))

    [event] = event_bus.published
    assert isinstance(event, PatientRegistered)
    assert event.patient_id == id
