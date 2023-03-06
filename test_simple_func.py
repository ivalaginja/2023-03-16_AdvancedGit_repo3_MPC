import run_me


def test_addition():
    this = run_me.add(5, 3)
    assert this == 8


def test_subtraction():
    that = run_me.subtract(10, 7)
    assert that == 3


def test_inverse():
    minuend = 6
    subtrahend = 4
    this = run_me.add(minuend, subtrahend)
    inv = run_me.subtract(this, minuend)
    assert inv == subtrahend
