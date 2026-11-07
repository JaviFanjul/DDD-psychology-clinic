from uuid import UUID

from core.infrastructure.postgres.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class PsychologistModel(Base):
    __tablename__ = "psychologists"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str]
    first_name: Mapped[str]
    last_names: Mapped[str]
    phone_prefix: Mapped[str]
    phone_number: Mapped[str]
    license_number: Mapped[str]
