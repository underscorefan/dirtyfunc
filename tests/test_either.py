from dirtyfunc import Left, Right, Either
from .run_async import run_async, arr_coro, simple_coro
import asyncio


def test_map():
    left = Left[str]("err")
    assert left.map(lambda x: x + 1).on_right() is None
    right = Right[str]("value")
    assert right.map(lambda x: x.upper()).on_right() == "VALUE"


def test_flat_map():
    def check_value(x: int, tr: int) -> Either[str, int]:
        return Right(x + 1) if x > tr else Left("error")

    right = Right[int](34)
    assert right.flat_map(lambda val: check_value(val, 30)).on_right() == 35
    new_r = right.flat_map(lambda val: check_value(val, 50))
    assert new_r.on_right() is None
    assert new_r.on_left() == "error"


def test_attempt():
    def raise_it():
        raise Exception("a")

    def not_raise_it():
        return 14

    attempt = Either.attempt(raise_it).map(lambda x: x + 1)
    assert attempt.on_left(lambda x: x.args[0]) == "a"
    assert attempt.on_right() is None

    new_attempt = Either.attempt(not_raise_it)
    assert new_attempt.on_left() is None
    assert new_attempt.on_right(lambda x: x + 1) == 15


def test_async():
    lst = [i for i in range(3)]
    add = 3

    async def r_coro():
        r = Right(right=lst)
        return await r.on_right_awaitable(lambda x: arr_coro(x, add))

    async def l_coro():
        left = Left(left=add)
        return await left.on_left_awaitable(lambda x: simple_coro(x))

    async def both():
        return await l_coro(), await r_coro()

    values = run_async(both)
    assert values[1] == [i + add for i in lst]
    assert values[0] == add * add


def test_empty():
    left = Left(1)
    assert left.empty is True


def test_attempt_awaitable():

    async def fail():
        await asyncio.sleep(1)
        raise ValueError

    async def attempt_it():
        return await Either.attempt_awaitable(fail())

    attempt = run_async(attempt_it)

    assert attempt.empty is True
