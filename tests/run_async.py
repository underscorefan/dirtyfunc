import asyncio

from typing import Callable, Any, List, Awaitable


async def simple_coro(x: int) -> int:
    await asyncio.sleep(1)
    return x * x


async def arr_coro(lst: List[int], add: int) -> List[int]:
    await asyncio.sleep(1)
    return [a + add for a in lst]


def run_async(f: Callable[[], Awaitable]) -> Any:
    loop = asyncio.get_event_loop()
    try:
        return loop.run_until_complete(f())
    finally:
        loop.close()
