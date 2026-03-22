from core.common.repositories.base.bulk import IMutableBulkRepository

from core.features.profiles.blocks.block import Block
from core.features.profiles.blocks.where import BlockWhere, BlockFilter


class IBlocksRepository(IMutableBulkRepository[Block, BlockWhere, BlockFilter]):
    pass
