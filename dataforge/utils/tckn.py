"""
TCKN (Türkiye Cumhuriyeti Kimlik Numarası) generator and validator.

Algorithm:
  - 11 digits
  - First digit cannot be 0
  - Digit 10 = (1*d1 + 3*d2 + 1*d3 + 3*d4 + 1*d5 + 3*d6 + 1*d7 + 3*d8 + 1*d9) % 10
  - Digit 11 = (d1+d2+d3+d4+d5+d6+d7+d8+d9+d10) % 10
"""
from __future__ import annotations
import random


def generate_tckn() -> str:
    """Generate a valid 11-digit TCKN string."""
    while True:
        # First 9 digits: d1 must not be 0
        digits = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(8)]

        # 10th digit
        d10 = (
            1 * digits[0] + 3 * digits[1] + 1 * digits[2] + 3 * digits[3]
            + 1 * digits[4] + 3 * digits[5] + 1 * digits[6] + 3 * digits[7]
            + 1 * digits[8]
        ) % 10
        digits.append(d10)

        # 11th digit
        d11 = sum(digits) % 10
        digits.append(d11)

        tckn = "".join(str(d) for d in digits)
        if is_valid_tckn(tckn):
            return tckn


def is_valid_tckn(tckn: str) -> bool:
    """Validate a TCKN string.

    Returns True if the TCKN passes all validity checks, False otherwise.
    """
    if not isinstance(tckn, str):
        return False
    if len(tckn) != 11:
        return False
    if not tckn.isdigit():
        return False
    digits = [int(c) for c in tckn]
    if digits[0] == 0:
        return False

    # Validate 10th digit (index 9)
    d10_expected = (
        1 * digits[0] + 3 * digits[1] + 1 * digits[2] + 3 * digits[3]
        + 1 * digits[4] + 3 * digits[5] + 1 * digits[6] + 3 * digits[7]
        + 1 * digits[8]
    ) % 10
    if digits[9] != d10_expected:
        return False

    # Validate 11th digit (index 10)
    d11_expected = sum(digits[:10]) % 10
    if digits[10] != d11_expected:
        return False

    return True
