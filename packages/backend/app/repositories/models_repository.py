from abc import ABC

from app.repositories.base import BaseRepository
from app.db.models.model import ModelORM
from app.domain.models.model import Model


class ModelsRepository(BaseRepository[ModelORM, Model], ABC):
    pass
