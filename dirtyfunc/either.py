from typing import TypeVar, Generic, Callable, Optional, Awaitable

L = TypeVar('L')
R = TypeVar('R')
T = TypeVar('T')


class Either(Generic[L, R]):

    C = TypeVar('C')

    def __init__(self, left: Optional[L], right: Optional[R]):
        self.__left = left
        self.__right = right

    def map(self, callback: Callable[[R], T]) -> 'Either[L, T]':
        return Either(self.__left, callback(self.__right)) if self.__right else self

    def flat_map(self, callback: Callable[[R], 'Either[L, T]']) -> 'Either[L, T]':
        return callback(self.__right) if self.__right else self

    def filter(self, callback: Callable[[R], bool]) -> 'Either[L, R]':
        return self if self.__right and callback(self.__right) else Left(self.__left)

    def on_left(self, callback: Callable[[L], T] = lambda x: x) -> Optional[T]:
        return self.__on_value(self.__left, callback)

    def on_right(self, callback: Callable[[R], T] = lambda x: x) -> Optional[T]:
        return self.__on_value(self.__right, callback)

    @property
    def empty(self) -> bool:
        return self.__right is None

    async def on_left_awaitable(self, callback: Callable[[L], Awaitable] = lambda x: x) -> Optional[Awaitable]:
        return await self.__on_value_awaitable(self.__left, callback)

    async def on_right_awaitable(self, callback: Callable[[R], Awaitable] = lambda x: x) -> Optional[Awaitable]:
        return await self.__on_value_awaitable(self.__right, callback)

    def __bool__(self):
        return self.__right is not None

    @staticmethod
    async def __on_value_awaitable(value: Optional[C], callback: Callable[[C], T]):
        return await callback(value) if value else None

    @staticmethod
    def __on_value(value: Optional[C], callback: Callable[[C], T]):
        return callback(value) if value else None

    @staticmethod
    def attempt(f: Callable[[], R]) -> 'Either[Exception, R]':
        try:
            return Right(f())
        except Exception as e:
            return Left(e)

    @staticmethod
    async def attempt_awaitable(awa: Awaitable[R]) -> 'Either[Exception, R]':
        try:
            return Right(await awa)
        except Exception as e:
            return Left(e)


class Left(Generic[L], Either[L, None]):
    def __init__(self, left: L):
        super().__init__(left, None)


class Right(Generic[R], Either[None, R]):
    def __init__(self, right: R):
        super().__init__(None, right)
