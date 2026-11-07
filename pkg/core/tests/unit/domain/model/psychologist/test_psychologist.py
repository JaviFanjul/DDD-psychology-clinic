from core.domain.model.psychologist.events import PsychologistCreated
from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId


def test_given_its_data_when_creating_then_the_psychologist_holds_it(
    psychologist_id,
    psychologist_email,
    psychologist_name,
    psychologist_phone,
    psychologist_license_number,
):
    psychologist = Psychologist.create(
        id=psychologist_id,
        email=psychologist_email,
        name=psychologist_name,
        phone=psychologist_phone,
        license_number=psychologist_license_number,
    )

    assert psychologist.id == psychologist_id
    assert psychologist.email == psychologist_email
    assert psychologist.name == psychologist_name
    assert psychologist.phone == psychologist_phone
    assert psychologist.license_number == psychologist_license_number


def test_given_a_created_psychologist_when_pulling_then_it_returns_psychologist_created(
    created_psychologist, psychologist_id
):
    [event] = created_psychologist.pull_events()

    assert isinstance(event, PsychologistCreated)
    assert event.psychologist_id == psychologist_id


def test_given_events_already_pulled_when_pulling_again_then_it_returns_no_events(
    created_psychologist,
):
    created_psychologist.pull_events()

    events = created_psychologist.pull_events()

    assert events == []


def test_given_a_psychologist_built_with_the_constructor_when_pulling_then_it_returns_no_events(
    psychologist_id,
    psychologist_email,
    psychologist_name,
    psychologist_phone,
    psychologist_license_number,
):
    psychologist = Psychologist(
        id=psychologist_id,
        email=psychologist_email,
        name=psychologist_name,
        phone=psychologist_phone,
        license_number=psychologist_license_number,
    )

    events = psychologist.pull_events()

    assert events == []


def test_given_two_psychologists_with_the_same_id_when_comparing_then_they_are_equal(
    created_psychologist,
    psychologist_id,
    psychologist_name,
    psychologist_phone,
    psychologist_license_number,
):
    same_psychologist = Psychologist(
        id=psychologist_id,
        email=PsychologistEmail(value="laura.martin@clinica.es"),
        name=psychologist_name,
        phone=psychologist_phone,
        license_number=psychologist_license_number,
    )

    assert same_psychologist == created_psychologist
    assert hash(same_psychologist) == hash(created_psychologist)


def test_given_two_psychologists_with_different_ids_when_comparing_then_they_are_not_equal(
    created_psychologist,
    psychologist_email,
    psychologist_name,
    psychologist_phone,
    psychologist_license_number,
):
    other_psychologist = Psychologist(
        id=PsychologistId.generate(),
        email=psychologist_email,
        name=psychologist_name,
        phone=psychologist_phone,
        license_number=psychologist_license_number,
    )

    assert other_psychologist != created_psychologist
