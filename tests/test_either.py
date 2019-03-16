from dirtyfunc import Left, Right, Either


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
