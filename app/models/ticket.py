import uuid

from sqlalchemy import String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        Enum(
            "low",
            "medium",
            "high",
            name="priority_enum"
        ),
        default="medium"
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "open",
            "in_progress",
            "resolved",
            "closed",
            name="status_enum"
        ),
        default="open"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    ) 

    assignee_email: Mapped[str] = mapped_column(
        String(254),
        nullable=True
    )