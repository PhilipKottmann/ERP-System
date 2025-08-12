import pytest
from controller import Controller

def test_division_method_standard():
    assert Controller.division_method(10, 2) == 5
    assert Controller.division_method(-12, 4) == -3
    assert Controller.division_method(100, 100) == 1

def test_division_method_float():
    assert Controller.division_method(1, 4) == 0.25
    assert Controller.division_method(10, 2.0) == 5.0
    assert pytest.approx(Controller.division_method(10, 3), 0.01) == 3.33

def test_division_method_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        Controller.division_method(5, 0)