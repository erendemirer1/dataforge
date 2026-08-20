"""
Tests for TCKN generation and validation.
"""
from dataforge.utils.tckn import generate_tckn, is_valid_tckn


def test_generate_valid_tckn():
    for _ in range(100):
        tckn = generate_tckn()
        assert is_valid_tckn(tckn), f"Generated invalid TCKN: {tckn}"


def test_tckn_length():
    for _ in range(20):
        tckn = generate_tckn()
        assert len(tckn) == 11, f"TCKN length != 11: {tckn}"


def test_tckn_first_digit_not_zero():
    for _ in range(50):
        tckn = generate_tckn()
        assert tckn[0] != '0', f"TCKN starts with 0: {tckn}"


def test_tckn_all_digits():
    for _ in range(20):
        tckn = generate_tckn()
        assert tckn.isdigit(), f"TCKN contains non-digit: {tckn}"


def test_invalid_tckn_wrong_length():
    assert not is_valid_tckn('12345678')
    assert not is_valid_tckn('123456789012')
    assert not is_valid_tckn('')


def test_invalid_tckn_starts_with_zero():
    # Manually construct a TCKN starting with 0
    assert not is_valid_tckn('01234567890')


def test_invalid_tckn_non_numeric():
    assert not is_valid_tckn('1234567890X')
    assert not is_valid_tckn('abcdefghijk')


def test_known_invalid_checksum():
    # All zeros except first digit
    assert not is_valid_tckn('10000000000')


def test_tckn_uniqueness():
    tckns = {generate_tckn() for _ in range(50)}
    # All 50 should be unique (astronomically likely)
    assert len(tckns) == 50


def test_is_valid_tckn_type_handling():
    assert not is_valid_tckn(None)  # type: ignore
    assert not is_valid_tckn(12345678901)  # type: ignore
