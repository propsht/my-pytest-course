import time
import datetime


def function_time_counter(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now() - start
        print(end)
        return result

    return wrapper


@function_time_counter
def fun1():
    time.sleep(2)


@function_time_counter
def fun2():
    time.sleep(1)


fun1()
fun2()
