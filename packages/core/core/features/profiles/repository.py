from core.common.repositories.base.mutable import IMutableRepository

from core.features.profiles.profile import Profile
from core.features.profiles.where import ProfileWhere, ProfileFilter


class IProfilesRepository(IMutableRepository[Profile, ProfileWhere, ProfileFilter]):
    pass
