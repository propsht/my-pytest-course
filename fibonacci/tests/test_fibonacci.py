from typing import Callable

import pytest

from fibonacci.cached import fibonacci_cached, fibonacci_lru_cached
from fibonacci.dynamic import fibonacci_dynamic, fibonacci_dynamic_v2
from fibonacci.naive import fibonacci_naive
from fibonacci.conftest import time_tracking


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (20, 6765),
    ],
)
# add parametrize decorator
@pytest.mark.parametrize(
    "fibonacci_func",
    [
        fibonacci_naive,
        fibonacci_cached,
        fibonacci_lru_cached,
        fibonacci_dynamic,
        fibonacci_dynamic_v2,
    ],
)
def test_fibonacci(
    time_tracking, fibonacci_func: Callable[[int], int], n: int, expected: int
) -> None:
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
