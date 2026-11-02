import pytest
from core.domain.model.patient.patient import Patient
from core.domain.model.patient.patient_address import PatientAddress
from core.domain.model.patient.patient_email import PatientEmail
from core.domain.model.patient.patient_id import PatientId
from core.domain.model.patient.patient_name import PatientName
from core.domain.model.patient.patient_phone import PatientPhone


@pytest.fixture
def patient_id() -> PatientId:
    return PatientId.generate()


@pytest.fixture
def patient_email() -> PatientEmail:
    return PatientEmail(value="ana@gmail.com")


@pytest.fixture
def patient_name() -> PatientName:
    return PatientName(first_name="Ana", last_names="García López")


@pytest.fixture
def patient_phone() -> PatientPhone:
    return PatientPhone(prefix="+34", number="612345678")


@pytest.fixture
def patient_address() -> PatientAddress:
    return PatientAddress(
        street="Calle Mayor 3, 2º B", postal_code="08001", city="Barcelona", province="Barcelona"
    )


@pytest.fixture
def created_patient(
    patient_id: PatientId,
    patient_email: PatientEmail,
    patient_name: PatientName,
    patient_phone: PatientPhone,
    patient_address: PatientAddress,
) -> Patient:
    return Patient.create(
        id=patient_id,
        email=patient_email,
        name=patient_name,
        phone=patient_phone,
        address=patient_address,
    )
