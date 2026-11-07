import pytest
from core.application.psychologist.command.create_psychologist import CreatePsychologistCommand
from core.domain.model.psychologist.events import PsychologistCreated
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone


@pytest.fixture
def command() -> CreatePsychologistCommand:
    return CreatePsychologistCommand(
        id=PsychologistId.generate(),
        email=PsychologistEmail(value="laura@clinica.es"),
        name=PsychologistName(first_name="Laura", last_names="Martín Ruiz"),
        phone=PsychologistPhone(prefix="+34", number="687654321"),
        license_number=PsychologistLicenseNumber(value="M-12345"),
    )


async def test_given_a_command_when_handling_then_the_psychologist_is_saved(
    create_psychologist_handler, psychologist_repository, command
):
    await create_psychologist_handler.handle(command=command)

    [psychologist] = psychologist_repository.saved
    assert psychologist.id == command.id
    assert psychologist.email == command.email
    assert psychologist.name == command.name
    assert psychologist.phone == command.phone
    assert psychologist.license_number == command.license_number


async def test_given_a_command_when_handling_then_psychologist_created_is_published(
    create_psychologist_handler, event_bus, command
):
    await create_psychologist_handler.handle(command=command)

    [event] = event_bus.published
    assert isinstance(event, PsychologistCreated)
    assert event.psychologist_id == command.id
