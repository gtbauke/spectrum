from typing import Callable, Awaitable, Union


type Provider[T] = Union[
    Callable[[], T],
    Callable[[], Awaitable[T]],
]

type Factory[T, D] = Callable[[D], T]
type AsyncFactory[T, D] = Callable[[D], Awaitable[T]]

type AnyFactory[T, D] = Union[
    Callable[[D], T],
    Callable[[D], Awaitable[T]],
]
