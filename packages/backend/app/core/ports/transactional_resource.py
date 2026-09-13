from typing import Protocol


class TransactionalResource(Protocol):
    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
