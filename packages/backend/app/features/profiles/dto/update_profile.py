from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from ..versions.dto.update_profile_version import UpdateProfileVersionDTO


class UpdateProfileDTO(BaseModel):
    owner_id: UUID
    version: Optional[UpdateProfileVersionDTO] = None
