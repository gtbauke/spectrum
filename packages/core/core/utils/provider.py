from typing import Callable, Awaitable, Union


type Provider[T] = Union[
    Callable[[], T],
    Callable[[], Awaitable[T]],
]

type Factory[T, D] = Union[
    Callable[[D], T],
    Callable[[D], Awaitable[T]],
]
