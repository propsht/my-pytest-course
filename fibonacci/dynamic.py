import sys


def fibonacci_dynamic(n: int) -> int:
    fibonacci_list = [0, 1]

    for i in range(1, n + 1):
        fibonacci_list.append(fibonacci_list[i] + fibonacci_list[i - 1])
        print(fibonacci_list)
    print(f"mem size of fibonacci_list is: {sys.getsizeof(fibonacci_list)}")

    return fibonacci_list[n]


def fibonacci_dynamic_v2(n: int) -> int:
    fib_1, fib_2 = 0, 1

    for i in range(1, n + 1):
        fi = fib_1 + fib_2
        fib_1, fib_2 = fib_2, fi

    return fib_1
