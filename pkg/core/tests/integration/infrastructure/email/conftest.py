import json
import time
from collections.abc import Iterator
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

import pytest
from core.domain.model.patient.patient_query_repository import PatientDto
from core.infrastructure.email.email_patient_notifier import EmailPatientNotifier
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
    )
