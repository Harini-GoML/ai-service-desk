from datetime import datetime
from uuid import UUID
from typing import Optional, Literal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    computed_field,
)

class CreateTicketRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    priority: Literal["low", "medium", "high"] = "medium"
    assignee_email: Optional[str] = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value

class UpdateTicketRequest(BaseModel):
    title: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[
        Literal["open", "in_progress", "resolved", "closed"]
    ] = None
    assignee_email: Optional[str] = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value

# class TicketResponse(BaseModel):
#     id: UUID
#     title: str
#     priority: Literal["low", "medium", "high"]
#     status: Literal["open", "in_progress", "resolved", "closed"]
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)

#     @computed_field
#     @property
#     def is_resolved(self) -> bool:
#         return self.status == "resolved"