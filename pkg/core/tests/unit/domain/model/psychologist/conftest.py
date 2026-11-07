import pytest
from core.domain.model.psychologist.psychologist import Psychologist
from core.domain.model.psychologist.psychologist_email import PsychologistEmail
from core.domain.model.psychologist.psychologist_id import PsychologistId
from core.domain.model.psychologist.psychologist_license_number import PsychologistLicenseNumber
from core.domain.model.psychologist.psychologist_name import PsychologistName
from core.domain.model.psychologist.psychologist_phone import PsychologistPhone


@pytest.fixture
def psychologist_id() -> PsychologistId:
    return PsychologistId.generate()


@pytest.fixture
def psychologist_email() -> PsychologistEmail:
    return PsychologistEmail(value="laura@clinica.es")


@pytest.fixture
def psychologist_name() -> PsychologistName:
    return PsychologistName(first_name="Laura", last_names="Martín Ruiz")


@pytest.fixture
def psychologist_phone() -> PsychologistPhone:
    return PsychologistPhone(prefix="+34", number="687654321")


@pytest.fixture
def psychologist_license_number() -> PsychologistLicenseNumber:
    return PsychologistLicenseNumber(value="M-12345")


@pytest.fixture
def created_psychologist(
    psychologist_id: PsychologistId,
    psychologist_email: PsychologistEmail,
    psychologist_name: PsychologistName,
    psychologist_phone: PsychologistPhone,
    psychologist_license_number: PsychologistLicenseNumber,
) -> Psychologist:
    return Psychologist.create(
        id=psychologist_id,
        email=psychologist_email,
        name=psychologist_name,
        phone=psychologist_phone,
        license_number=psychologist_license_number,
    )
