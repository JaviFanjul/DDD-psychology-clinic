from typing import Any
from uuid import UUID

from assistant.infrastructure.postgres.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class ConversationModel(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    patient_id: Mapped[UUID]
    messages: Mapped[list[dict[str, Any]]] = mapped_column(JSONB)
