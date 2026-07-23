from typing import Optional, Literal

from pydantic import (BaseModel,Field,field_validator)

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
    
class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5_000)
 
 
class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str