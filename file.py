def plus(a: str, b):
    return a + b


def without(*args):
    print('some text')
    return 1


def onlytuple(tuple):
    assert type(tuple) == tuple


def passall(nothing):
    pass


def division(a):
    print(a/0)
