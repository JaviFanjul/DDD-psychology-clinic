from datetime import datetime
from uuid import UUID

from core.infrastructure.postgres.base import Base
from core.infrastructure.postgres.patient_model import PatientModel
from core.infrastructure.postgres.psychologist_model import PsychologistModel
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class AppointmentModel(Base):
    __tablename__ = "appointments"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    patient_id: Mapped[UUID] = mapped_column(ForeignKey(PatientModel.id))
    psychologist_id: Mapped[UUID] = mapped_column(ForeignKey(PsychologistModel.id), index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int]
    modality: Mapped[str]
    status: Mapped[str]
