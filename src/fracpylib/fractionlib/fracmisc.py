"""Class for other (misc) functions"""
from __future__ import annotations
from numbers import Integral
from typing import TYPE_CHECKING

from .fracmath import FracMath

if TYPE_CHECKING:
    from fracpylib.fractionlib.fraction import Fraction


class FracMisc:
    @staticmethod
    def is_power_of_10(n: int) -> bool:
        """Return True when n is exactly 1, 10, 100, and so on."""
        if not isinstance(n, Integral) or isinstance(n, bool):
            return False
        n = int(n)
        if n <= 0:
            return False
        while n % 10 == 0:
            n //= 10
        return n == 1

    @staticmethod
    def is_proper(frac: Fraction) -> bool:
        """Return True when abs(numerator) is smaller than denominator."""
        frac = FracMisc._as_fraction(frac)
        return abs(frac.numerator) < frac.denominator

    @staticmethod
    def is_improper(frac: Fraction) -> bool:
        """Return True when abs(numerator) is greater than or equal to denominator."""
        frac = FracMisc._as_fraction(frac)
        return abs(frac.numerator) >= frac.denominator

    @staticmethod
    def is_integer(frac: Fraction) -> bool:
        """Return True when the fraction has no fractional part."""
        frac = FracMisc._as_fraction(frac)
        return frac.denominator == 1

    @staticmethod
    def is_unit(frac: Fraction) -> bool:
        """Return True for fractions with absolute numerator 1."""
        frac = FracMisc._as_fraction(frac)
        return abs(frac.numerator) == 1

    @staticmethod
    def is_terminating(frac: Fraction) -> bool:
        """Return True when the fraction has a finite decimal expansion."""
        frac = FracMisc._as_fraction(frac)
        denominator = frac.denominator
        for factor in (2, 5):
            while denominator % factor == 0:
                denominator //= factor
        return denominator == 1

    @staticmethod
    def has_repeating_decimal(frac: Fraction) -> bool:
        """Return True when the decimal expansion repeats forever."""
        return not FracMisc.is_terminating(frac)

    @staticmethod
    def _as_fraction(frac: Fraction) -> Fraction:
        fraction = FracMath.as_fraction(frac)
        if fraction is NotImplemented:
            raise TypeError("Expected a Fraction-compatible value.")
        return fraction

    # Backward-compatible camelCase aliases.
    isProper = is_proper
    isImproper = is_improper
