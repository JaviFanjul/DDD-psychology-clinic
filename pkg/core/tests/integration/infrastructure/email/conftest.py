import json
import time
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

import pytest
from core.domain.model.appointment.appointment_query_repository import AppointmentDto
from core.domain.model.patient.patient_query_repository import PatientDto
from core.domain.model.psychologist.psychologist_query_repository import PsychologistDto
from core.infrastructure.email.email_patient_notifier import EmailPatientNotifier
from core.infrastructure.email.email_psychologist_notifier import EmailPsychologistNotifier
from testcontainers.community.mailpit import MailpitContainer

MAILPIT_IMAGE = "axllent/mailpit:v1.33.0"
SENDER = "clinica@example.com"
READY_TIMEOUT_SECONDS = 30


class Mailbox:
    def __init__(self, api_url: str) -> None:
        self._api_url = api_url

    def messages(self) -> list[dict[str, Any]]:
        summaries = self._get(path="/api/v1/messages")["messages"]
        return [self._get(path=f"/api/v1/message/{summary['ID']}") for summary in summaries]

    def wait_until_ready(self) -> None:
        deadline = time.monotonic() + READY_TIMEOUT_SECONDS
        while True:
            try:
                self.messages()
                return
            except URLError, ConnectionError:
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.5)

    def clear(self) -> None:
        urlopen(Request(f"{self._api_url}/api/v1/messages", method="DELETE"))

    def _get(self, path: str) -> dict[str, Any]:
        with urlopen(f"{self._api_url}{path}") as response:
            return json.load(response)


@pytest.fixture(scope="session")
def mailpit() -> Iterator[MailpitContainer]:
    with MailpitContainer(image=MAILPIT_IMAGE) as container:
        Mailbox(api_url=container.get_base_api_url()).wait_until_ready()
        yield container


@pytest.fixture
def mailbox(mailpit: MailpitContainer) -> Iterator[Mailbox]:
    mailbox = Mailbox(api_url=mailpit.get_base_api_url())
    yield mailbox
    mailbox.clear()


@pytest.fixture
def notifier(mailpit: MailpitContainer) -> EmailPatientNotifier:
    return EmailPatientNotifier(
        host=mailpit.get_container_host_ip(),
        port=mailpit.get_exposed_smtp_port(),
        username="clinica",
        password="secret",
        sender=SENDER,
        validate_certs=False,
    )


@pytest.fixture
def patient() -> PatientDto:
    return PatientDto(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        email="ana@gmail.com",
        first_name="Ana",
        last_names="García López",
        phone_prefix="+34",
        phone_number="612345678",
        street="Calle Mayor 3, 2º B",
        postal_code="08001",
        city="Barcelona",
        province="Barcelona",
        status="active",
    )


@pytest.fixture
def psychologist_notifier(mailpit: MailpitContainer) -> EmailPsychologistNotifier:
    return EmailPsychologistNotifier(
        host=mailpit.get_container_host_ip(),
        port=mailpit.get_exposed_smtp_port(),
        username="clinica",
        password="secret",
        sender=SENDER,
        validate_certs=False,
    )


@pytest.fixture
def psychologist() -> PsychologistDto:
    return PsychologistDto(
        id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        email="laura@clinica.es",
        first_name="Laura",
        last_names="Martín Ruiz",
        phone_prefix="+34",
        phone_number="687654321",
        license_number="M-12345",
    )


@pytest.fixture
def appointment() -> AppointmentDto:
    return AppointmentDto(
        id="3f2504e0-4f89-41d3-9a0c-0305e82c3301",
        patient_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        psychologist_id="0b1f2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
        starts_at=datetime(year=2026, month=11, day=10, hour=9, tzinfo=UTC),
        duration_minutes=50,
        modality="in_person",
        status="pending",
    )
