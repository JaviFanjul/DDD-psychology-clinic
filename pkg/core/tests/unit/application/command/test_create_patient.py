from core.application.command.create_patient import CreatePatientCommand
from core.domain.model.patient.events import PatientCreated
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId


async def test_given_a_command_when_handling_then_the_patient_is_saved(
    handler, repository, patient_name, patient_phone, patient_address
):
    id = PatientId.generate()
    email = PatientEmail(value="ana@gmail.com")

    await handler.handle(
        command=CreatePatientCommand(
            id=id, email=email, name=patient_name, phone=patient_phone, address=patient_address
        )
    )

    [patient] = repository.saved
    assert patient.id == id
    assert patient.email == email
    assert patient.name == patient_name
    assert patient.phone == patient_phone
    assert patient.address == patient_address


async def test_given_a_command_when_handling_then_patient_created_is_published(
    handler, event_bus, patient_name, patient_phone, patient_address
):
    id = PatientId.generate()

    await handler.handle(
        command=CreatePatientCommand(
            id=id,
            email=PatientEmail(value="ana@gmail.com"),
            name=patient_name,
            phone=patient_phone,
            address=patient_address,
        )
    )

    [event] = event_bus.published
    assert isinstance(event, PatientCreated)
    assert event.patient_id == id
