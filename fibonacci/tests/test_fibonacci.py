from typing import Callable

import pytest

from fibonacci.cached import fibonacci_cached
from fibonacci.naive import fibonacci_naive


# add parametrize decorator
@pytest.mark.parametrize("fibonacci_func", [fibonacci_naive, fibonacci_cached])
@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (20, 6765),
    ],
)
def test_fibonacci(fibonacci_func: Callable[[int], int], n: int, expected: int) -> None:
    res = fibonacci_func(n)
    assert res == expected


# @pytest.mark.parametrize("n,expected",[(0, 0),(1, 1),(2, 1),(20, 6765),],)
# def test_naive(n: int, expected: int) -> None:
#     res = fibonacci_naive(n=n)
#     assert res == expected


# @pytest.mark.parametrize("n,expected", [(0, 0),(1, 1),(2, 1), (20, 6765),],)
# def test_cached(n: int, expected: int) -> None:
#     res = fibonacci_cached(n=n)
#     assert res == expected
