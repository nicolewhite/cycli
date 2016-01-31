from cycli.table import isnumeric, col_widths
import pytest

@pytest.mark.parametrize(("number", "answer"), [
    ("12", True),
    ("12.3", True),
    ("0", True),
    ("1.1.0", False),
    ("Hell0", False),
    ("Hello", False)
])
def test_isnumeric(number, answer):
    assert isnumeric(number) == answer

@pytest.mark.parametrize(("headers", "rows", "answer"), [
    (["a", "bc"], [["a", "b"], ["a", "b"]], [1, 2]),
    (["ab", "c"], [["a", "b"], ["a", "b"]], [2, 1]),
    (["a", "b"], [["a", "bc"], ["a", "b"]], [1, 2]),
    (["a", "b"], [["ab", "c"], ["a", "b"]], [2, 1]),
    (["a", "b"], [["", ""], ["a", "a"]], [1, 1])
])
def test_col_widths(headers, rows, answer):
    assert col_widths(headers, rows) == answer