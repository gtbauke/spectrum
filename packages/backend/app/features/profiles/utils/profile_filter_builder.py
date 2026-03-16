from typing import Optional
from uuid import UUID
from fastapi import Depends, Query

from app.features.auth.guards.get_current_user import get_optional_current_owner

from core.models.profiles.profile_dataset_role import ProfileDatasetRole
from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility
from core.models.profiles.where import ProfileDatasetAssociationFilter, ProfileFilter, ProfileVersionFilter
from core.utils.filters.field_filter import EnumFilter, NumberFilter, StringFilter, UUIDFilter


class ProfileFilterBuilder:
    def __init__(
        self,
        owner_id: Optional[UUID] = Depends(get_optional_current_owner),
        version: Optional[int] = Query(None),
        name: Optional[str] = Query(None),
        description: Optional[str] = Query(None),
        status: ProfileStatus = Query(ProfileStatus.ACTIVE),
        visibility: ProfileVisibility = Query(ProfileVisibility.PUBLIC),
        role: Optional[ProfileDatasetRole] = Query(None),
        only_me: bool = Query(False),
    ):
        self._owner_id = owner_id
        self._version = version
        self._name = name
        self._description = description
        self._status = status
        self._visibility = visibility
        self._role = role
        self._only_me = only_me

    def build(self) -> ProfileFilter:
        datasets_filter = ProfileDatasetAssociationFilter(
            role=EnumFilter[ProfileDatasetRole](eq=self._role),
        ) if self._role else None

        versions_filter = ProfileVersionFilter(
            version=NumberFilter[int](
                eq=self._version) if self._version is not None else None,
            name=StringFilter(ilike=f"%{self._name}%") if self._name else None,
            description=StringFilter(
                ilike=f"%{self._description}%") if self._description else None,
            status=EnumFilter[ProfileStatus](
                eq=self._status) if self._status else None,
            datasets=datasets_filter
        )

        if self._only_me:
            final_filter = ProfileFilter(
                owner_id=UUIDFilter(eq=self._owner_id),
                versions=versions_filter.model_copy(
                    update={
                        "visibility": EnumFilter[ProfileVisibility](eq=self._visibility)
                    }
                )
            )
        else:
            public_versions = versions_filter.model_copy(
                update={
                    "visibility": EnumFilter[ProfileVisibility](eq=self._visibility)
                }
            )

            final_filter = ProfileFilter(
                OR=[
                    ProfileFilter(versions=public_versions),
                    ProfileFilter(
                        owner_id=UUIDFilter(eq=self._owner_id),
                        versions=versions_filter,
                    )
                ]
            )

        return final_filter
