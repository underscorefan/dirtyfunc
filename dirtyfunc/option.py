from typing import TypeVar, Generic, Callable, Optional, Awaitable

T = TypeVar('T')
Y = TypeVar('Y')
E = TypeVar('E')


class Option(Generic[T]):

    def __init__(self, val: Optional[T]):
        self.__val = val

    def map(self, callback: Callable[[T], Y]) -> 'Option[Y]':
        return Option(callback(self.__val)) if self.__val else Nothing()

    def flat_map(self, callback: Callable[[T], 'Option[Y]']) -> 'Option[Y]':
        value = self.map(callback).__val
        return value if value else Nothing()

    def filter(self, callback: Callable[[T], bool]) -> 'Option[T]':
        return self if self.map(callback).__val else Nothing()

    def on_value(self, callback: Callable[[T], Y] = lambda x: x) -> Optional[Y]:
        return callback(self.__val) if self.__val else None

    async def on_value_awaitable(self, callback: Callable[[T], Awaitable[Y]] = lambda x: x):
        return await callback(self.__val) if self.__val else None

    def __bool__(self) -> bool:
        return self.__val is not None


class Nothing(Option[None]):
    def __init__(self):
        super().__init__(None)
