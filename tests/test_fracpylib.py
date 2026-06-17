from decimal import Decimal

import pytest

from fracpylib.fraction import Fraction, FracMath, FracMisc, MixedFraction
from fracpylib.fraction.fraction import FracMath as ReExportedFracMath




def test_fraction_strings_repr_and_hashing():
    assert str(Fraction(3, 4)) == "3/4"
    assert str(Fraction(4, 2)) == "2"
    assert repr(Fraction(2, 4)) == "Fraction(1, 2)"
    assert len({Fraction(1, 2), Fraction(2, 4)}) == 1

    with pytest.raises(AttributeError):
        Fraction(1, 2).numerator = 3


def test_fraction_arithmetic_accepts_integers():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
    assert Fraction(1, 2) + 1 == Fraction(3, 2)
    assert 1 + Fraction(1, 2) == Fraction(3, 2)
    assert 1 - Fraction(3, 4) == Fraction(1, 4)
    assert 2 * Fraction(3, 4) == Fraction(3, 2)
    assert 3 / Fraction(3, 2) == Fraction(2, 1)


def test_fraction_extra_numeric_features():
    assert Fraction(2, 3) ** -2 == Fraction(9, 4)
    assert Fraction(-3, 2).reciprocal() == Fraction(-2, 3)
    assert int(Fraction(-3, 2)) == -1
    assert bool(Fraction(0, 5)) is False
    assert Fraction(4, 2).is_integer() is True

    with pytest.raises(ZeroDivisionError):
        Fraction(0, 1).reciprocal()


def test_fraction_comparisons_accept_mixed_and_ints():
    assert Fraction(3, 2) == MixedFraction(1, 1, 2)
    assert Fraction(3, 2) > 1
    assert MixedFraction(1, 1, 2) >= Fraction(3, 2)


def test_mixed_fraction_math_with_other_numeric_types():
    mf = MixedFraction(1, 1, 2)
    assert mf + Fraction(1, 6) == Fraction(5, 3)
    assert 2 - mf == Fraction(1, 2)
    assert mf * 2 == Fraction(3, 1)
    assert 3 / mf == Fraction(2, 1)


def test_fracmath_simplify_amplify_and_reexport():
    assert ReExportedFracMath is FracMath
    assert FracMath.simplify(Fraction(4, 8), Recurse=True) == Fraction(1, 2)
    assert FracMath.simplify(Fraction(4, 8), Recurse=False, Value=1) == Fraction(1, 2)
    assert FracMath.amplify(Fraction(1, 3), 4) == Fraction(1, 3)

    with pytest.raises(ValueError):
        FracMath.amplify(Fraction(1, 3), 0)


def test_periodic_decimal_creation_from_parts_and_strings():
    assert FracMath.from_periodic(whole=0, non_repeating="", repeating="3") == Fraction(1, 3)
    assert Fraction.from_periodic(whole=1, non_repeating="1", repeating="6") == Fraction(7, 6)
    assert Fraction.from_periodic(whole=0, non_repeating="1", repeating="6", sign=-1) == Fraction(-1, 6)
    assert Fraction.from_decimal("0.(09)") == Fraction(1, 11)
    assert Fraction.from_decimal("-1.1(6)") == Fraction(-7, 6)
    assert Fraction.from_decimal(".125") == Fraction(1, 8)
    assert Fraction.from_decimal(Decimal("1.20")) == Fraction(6, 5)
    assert Fraction.from_decimal(0.1) == Fraction(1, 10)

    with pytest.raises(ValueError):
        Fraction.from_decimal("1.(x)")


def test_periodic_decimal_rendering():
    assert Fraction(1, 2).to_periodic() == "0.5"
    assert Fraction(1, 3).to_periodic() == "0.(3)"
    assert Fraction(1, 6).to_periodic() == "0.1(6)"
    assert Fraction(-22, 7).to_periodic() == "-3.(142857)"
    assert MixedFraction(1, 1, 6).to_periodic() == "1.1(6)"


def test_fracmisc_helpers():
    assert FracMisc.is_power_of_10(1000) is True
    assert FracMisc.is_power_of_10(20) is False
    assert FracMisc.isProper(Fraction(2, 3)) is True
    assert FracMisc.is_improper(Fraction(3, 2)) is True
    assert FracMisc.is_integer(Fraction(8, 4)) is True
    assert FracMisc.is_unit(Fraction(-1, 7)) is True
    assert FracMisc.is_terminating(Fraction(1, 8)) is True
    assert FracMisc.has_repeating_decimal(Fraction(1, 3)) is True
