from uuid import UUID

from assistant.infrastructure.postgres.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class PatientModel(Base):
    __tablename__ = "patients"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    active: Mapped[bool]
