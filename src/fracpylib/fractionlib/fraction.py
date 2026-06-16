from __future__ import annotations
import math
from numbers import Integral
from typing import Tuple, cast

from .fracmath import FracMath


class Fraction:
    __slots__ = ('numerator', 'denominator')

    def __init__(self, numerator: int, denominator: int):
        if not isinstance(numerator, Integral) or isinstance(numerator, bool):
            raise TypeError("Numerator must be an integer.")
        if not isinstance(denominator, Integral) or isinstance(denominator, bool):
            raise TypeError("Denominator must be an integer.")

        numerator = int(numerator)
        denominator = int(denominator)
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")

        if numerator == 0:
            self.numerator = 0
            self.denominator = 1
            return

        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        divisor = math.gcd(abs(numerator), denominator)
        self.numerator = numerator // divisor
        self.denominator = denominator // divisor

    def __str__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"

    def __setattr__(self, name: str, value: object) -> None:
        if name in self.__slots__ and hasattr(self, name):
            raise AttributeError("Fraction instances are immutable.")
        super().__setattr__(name, value)

    def __hash__(self) -> int:
        return hash((self.numerator, self.denominator))

    def __bool__(self) -> bool:
        return self.numerator != 0

    def __add__(self, other: object) -> Fraction:
        return FracMath.add(self, other)

    def __radd__(self, other: object) -> Fraction:
        return FracMath.add(other, self)

    def __sub__(self, other: object) -> Fraction:
        return FracMath.sub(self, other)

    def __rsub__(self, other: object) -> Fraction:
        return FracMath.sub(other, self)

    def __mul__(self, other: object) -> Fraction:
        return FracMath.multiply(self, other)

    def __rmul__(self, other: object) -> Fraction:
        return FracMath.multiply(other, self)

    def __truediv__(self, other: object) -> Fraction:
        return FracMath.divide(self, other)

    def __rtruediv__(self, other: object) -> Fraction:
        return FracMath.divide(other, self)

    def __neg__(self) -> Fraction:
        return Fraction(-self.numerator, self.denominator)

    def __pos__(self) -> Fraction:
        return self

    def __abs__(self) -> Fraction:
        return Fraction(abs(self.numerator), self.denominator)

    def __pow__(self, power: int) -> Fraction:
        if not isinstance(power, Integral) or isinstance(power, bool):
            raise TypeError("Power must be an integer.")

        power = int(power)
        if power == 0:
            return Fraction(1, 1)
        if power < 0:
            if self.numerator == 0:
                raise ZeroDivisionError("Cannot raise zero to a negative power.")
            power = abs(power)
            return Fraction(self.denominator ** power, self.numerator ** power)
        return Fraction(self.numerator ** power, self.denominator ** power)

    def __float__(self) -> float:
        return self.numerator / self.denominator

    def __int__(self) -> int:
        if self.numerator >= 0:
            return self.numerator // self.denominator
        return -((-self.numerator) // self.denominator)

    def __eq__(self, other: object) -> bool:
        other_fraction = FracMath.as_fraction(other)
        if other_fraction is NotImplemented:
            return NotImplemented
        return (
            self.numerator == other_fraction.numerator
            and self.denominator == other_fraction.denominator
        )

    def __lt__(self, other: object) -> bool:
        other_fraction = FracMath.as_fraction(other)
        if other_fraction is NotImplemented:
            return NotImplemented
        return self.numerator * other_fraction.denominator < other_fraction.numerator * self.denominator

    def __le__(self, other: object) -> bool:
        other_fraction = FracMath.as_fraction(other)
        if other_fraction is NotImplemented:
            return NotImplemented
        return self.numerator * other_fraction.denominator <= other_fraction.numerator * self.denominator

    def __gt__(self, other: object) -> bool:
        other_fraction = FracMath.as_fraction(other)
        if other_fraction is NotImplemented:
            return NotImplemented
        return self.numerator * other_fraction.denominator > other_fraction.numerator * self.denominator

    def __ge__(self, other: object) -> bool:
        other_fraction = FracMath.as_fraction(other)
        if other_fraction is NotImplemented:
            return NotImplemented
        return self.numerator * other_fraction.denominator >= other_fraction.numerator * self.denominator

    @classmethod
    def from_decimal(cls, value: object) -> Fraction:
        """Create a Fraction from a finite or periodic decimal value."""
        return FracMath.from_decimal(value)

    @classmethod
    def from_periodic(
        cls,
        whole: int = 0,
        non_repeating: str = "",
        repeating: str = "",
        sign: int = 0,
    ) -> Fraction:
        """Create a Fraction from pieces of a periodic decimal."""
        return FracMath.from_periodic(whole, non_repeating, repeating, sign)

    def reciprocal(self) -> Fraction:
        """Return the multiplicative inverse of this fraction."""
        if self.numerator == 0:
            raise ZeroDivisionError("Zero does not have a reciprocal.")
        return Fraction(self.denominator, self.numerator)

    def is_integer(self) -> bool:
        return self.denominator == 1

    def as_tuple(self) -> Tuple[int, int]:
        return self.numerator, self.denominator

    def to_mixed(self) -> MixedFraction:
        return MixedFraction.from_fraction(self)

    def to_periodic(self) -> str:
        """Return the exact finite or repeating decimal representation."""
        return FracMath.to_periodic(self)

    def to_decimal(self) -> str:
        """Alias for to_periodic()."""
        return self.to_periodic()


class MixedFraction:
    __slots__ = ('whole', 'numerator', 'denominator', 'converted')

    def __init__(self, whole: int, numerator: int, denominator: int):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")

        self._set_from_fraction(FracMath.mixedToNormal(whole, numerator, denominator))

    def __str__(self) -> str:
        if self.numerator == 0:
            return str(self.whole)
        if self.whole == 0:
            return f"{self.numerator}/{self.denominator}"
        return f"{self.whole} {self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        return f"MixedFraction({self.whole}, {self.numerator}, {self.denominator})"

    def __add__(self, other: object) -> Fraction:
        return FracMath.add(self.converted, other)

    def __radd__(self, other: object) -> Fraction:
        return FracMath.add(other, self.converted)

    def __sub__(self, other: object) -> Fraction:
        return FracMath.sub(self.converted, other)

    def __rsub__(self, other: object) -> Fraction:
        return FracMath.sub(other, self.converted)

    def __mul__(self, other: object) -> Fraction:
        return FracMath.multiply(self.converted, other)

    def __rmul__(self, other: object) -> Fraction:
        return FracMath.multiply(other, self.converted)

    def __truediv__(self, other: object) -> Fraction:
        return FracMath.divide(self.converted, cast(Fraction, other))

    def __rtruediv__(self, other: object) -> Fraction:
        return FracMath.divide(cast(Fraction, other), self.converted)

    def __neg__(self) -> MixedFraction:
        return MixedFraction.from_fraction(-self.converted)

    def __abs__(self) -> MixedFraction:
        return MixedFraction.from_fraction(abs(self.converted))

    def __bool__(self) -> bool:
        return bool(self.converted)

    def __float__(self) -> float:
        return float(self.converted)

    def __eq__(self, other: object) -> bool:
        other_fraction = FracMath.as_fraction(other)
        if other_fraction is NotImplemented:
            return NotImplemented
        return self.converted == other_fraction

    def __lt__(self, other: object) -> bool:
        return self.converted < other

    def __le__(self, other: object) -> bool:
        return self.converted <= other

    def __gt__(self, other: object) -> bool:
        return self.converted > other

    def __ge__(self, other: object) -> bool:
        return self.converted >= other

    @classmethod
    def from_fraction(cls, fraction: object) -> MixedFraction:
        converted = FracMath.as_fraction(fraction)
        if converted is NotImplemented:
            raise TypeError("Expected a Fraction-compatible value.")

        mixed = cls.__new__(cls)
        mixed._set_from_fraction(converted)
        return mixed

    def to_fraction(self) -> Fraction:
        return self.converted

    def to_periodic(self) -> str:
        return self.converted.to_periodic()

    def _set_from_fraction(self, fraction: Fraction) -> None:
        self.converted = fraction
        self.whole, self.numerator, self.denominator = self._parts_from_fraction(fraction)

    @staticmethod
    def _parts_from_fraction(fraction: Fraction) -> Tuple[int, int, int]:
        sign = -1 if fraction.numerator < 0 else 1
        whole, numerator = divmod(abs(fraction.numerator), fraction.denominator)
        if sign < 0 and whole:
            return -whole, numerator, fraction.denominator
        if sign < 0:
            return 0, -numerator, fraction.denominator
        return whole, numerator, fraction.denominator
