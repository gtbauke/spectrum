from core.common.repositories.base.mutable import IMutableRepository

from core.features.profiles.blocks.block import Block
from core.features.profiles.blocks.where import BlockWhere, BlockFilter


class IBlocksRepository(IMutableRepository[Block, BlockWhere, BlockFilter]):
    pass
