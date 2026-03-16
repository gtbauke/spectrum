from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime


class UserDetails(BaseModel):
    id: UUID = Field(..., description="ID of the user")

    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")

    email: EmailStr = Field(...,
                            description="Email associated with the user account")

    created_at: datetime = Field(...,
                                 description="Date and time the user was created")

    updated_at: datetime = Field(...,
                                 description="Date and time the user was updated")

    deleted_at: Optional[datetime] = Field(...,
                                           description="Date and time the user was deleted")
