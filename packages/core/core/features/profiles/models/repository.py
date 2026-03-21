from core.common.repositories.base.mutable import IMutableRepository

from core.features.profiles.models.model import Model
from core.features.profiles.models.where import ModelWhere, ModelFilter


class IModelsRepository(IMutableRepository[Model, ModelWhere, ModelFilter]):
    pass
