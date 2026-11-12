import pytest

from bug3_logic import find_max


def test_example_input_uses_the_value_returned_by_the_supplied_code():
    # This intentionally records the buggy output; the correct maximum is 95.
    assert find_max([70, 85, 60, 95]) == 85


def test_descending_input_returns_the_first_value():
    assert find_max([95, 85, 70, 60]) == 95


def test_single_value_is_its_own_maximum():
    assert find_max([42]) == 42


def test_empty_input_raises_index_error():
    with pytest.raises(IndexError):
        find_max([])