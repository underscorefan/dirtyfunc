from dirtyfunc import Option, Nothing
from .run_async import run_async, simple_coro


def test_map():
    a = Option(3)
    assert a.map(lambda x: x + 1).on_value() == 4


def test_bool():
    a = Nothing()
    assert bool(a) is False
    b = Option(124)
    assert bool(b) is True


def test_flat_map():
    a = Option(3)
    assert a.flat_map(lambda x: Option(x + 1)).on_value() == 4
    b = Nothing()
    assert bool(b.flat_map(lambda x: Option(x + 1))) is False


def test_filter():
    a = Option(True)
    assert a.filter(lambda x: x).on_value() is True
    b = Option(42)
    assert b.filter(lambda x: x > 40).on_value() == 42
    assert b.filter(lambda x: x > 50).on_value() is None


def test_value_async():
    num = 2

    async def opt():
        a = Option(num)
        return await a.on_value_awaitable(lambda val: simple_coro(val))

    assert run_async(opt) == num * num


def test_empty():
    empty = Nothing()
    assert empty.empty is True
