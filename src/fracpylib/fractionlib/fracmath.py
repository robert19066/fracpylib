from __future__ import annotations
from decimal import Decimal, InvalidOperation
import math
from numbers import Integral
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fracpylib.fractionlib.fraction import Fraction


class FracMath:
    """Stateless helpers for exact fraction arithmetic."""

    @staticmethod
    def as_fraction(value: object) -> Fraction:
        """Return *value* as a Fraction, or NotImplemented for unsupported inputs."""
        from fracpylib.fractionlib.fraction import Fraction, MixedFraction

        if isinstance(value, Fraction):
            return value
        if isinstance(value, MixedFraction):
            return value.converted
        if isinstance(value, Integral) and not isinstance(value, bool):
            return Fraction(int(value), 1)
        return NotImplemented

    @staticmethod
    def simplify(fraction: object, Recurse: bool = True, Value: int = 0) -> Fraction:
        """Return a fraction in lowest terms, or divide by a known common divisor."""
        from fracpylib.fractionlib.fraction import Fraction

        fraction = FracMath.as_fraction(fraction)
        if fraction is NotImplemented:
            raise TypeError("Expected a Fraction-compatible value.")

        if Recurse:
            return Fraction(fraction.numerator, fraction.denominator)

        if not isinstance(Value, Integral) or isinstance(Value, bool):
            raise TypeError("Simplification value must be an integer.")

        Value = abs(int(Value))
        if Value == 0:
            raise ValueError("Cannot simplify with a value of 0.")

        if (fraction.numerator % Value == 0) and (fraction.denominator % Value == 0):
            return Fraction(fraction.numerator // Value, fraction.denominator // Value)

        raise ValueError(f"The value {Value} must be a common divisor.")

    @staticmethod
    def amplify(fraction: object, Value: int) -> Fraction:
        """Multiply numerator and denominator by the same non-zero integer."""
        from fracpylib.fractionlib.fraction import Fraction

        fraction = FracMath.as_fraction(fraction)
        if fraction is NotImplemented:
            raise TypeError("Expected a Fraction-compatible value.")
        if not isinstance(Value, Integral) or isinstance(Value, bool):
            raise TypeError("Amplification value must be an integer.")
        if Value == 0:
            raise ValueError("Amplification value cannot be zero.")

        return Fraction(fraction.numerator * Value, fraction.denominator * Value)

    @staticmethod
    def add(fraction1: object, fraction2: object) -> Fraction:
        """Add two Fraction-compatible values."""
        from fracpylib.fractionlib.fraction import Fraction

        fraction1 = FracMath.as_fraction(fraction1)
        fraction2 = FracMath.as_fraction(fraction2)
        if fraction1 is NotImplemented or fraction2 is NotImplemented:
            return NotImplemented

        gcd = math.gcd(fraction1.denominator, fraction2.denominator)
        left_scale = fraction2.denominator // gcd
        right_scale = fraction1.denominator // gcd
        new_numerator = (fraction1.numerator * left_scale) + (fraction2.numerator * right_scale)
        new_denominator = fraction1.denominator * left_scale
        return FracMath.simplify(Fraction(new_numerator, new_denominator))

    @staticmethod
    def sub(fraction1: object, fraction2: object) -> Fraction:
        """Subtract the second Fraction-compatible value from the first."""
        from fracpylib.fractionlib.fraction import Fraction

        fraction1 = FracMath.as_fraction(fraction1)
        fraction2 = FracMath.as_fraction(fraction2)
        if fraction1 is NotImplemented or fraction2 is NotImplemented:
            return NotImplemented

        gcd = math.gcd(fraction1.denominator, fraction2.denominator)
        left_scale = fraction2.denominator // gcd
        right_scale = fraction1.denominator // gcd
        new_numerator = (fraction1.numerator * left_scale) - (fraction2.numerator * right_scale)
        new_denominator = fraction1.denominator * left_scale
        return FracMath.simplify(Fraction(new_numerator, new_denominator))

    @staticmethod
    def multiply(fraction1: object, fraction2: object) -> Fraction:
        """Multiply two Fraction-compatible values."""
        from fracpylib.fractionlib.fraction import Fraction

        fraction1 = FracMath.as_fraction(fraction1)
        fraction2 = FracMath.as_fraction(fraction2)
        if fraction1 is NotImplemented or fraction2 is NotImplemented:
            return NotImplemented

        gcd1 = math.gcd(abs(fraction1.numerator), fraction2.denominator)
        gcd2 = math.gcd(abs(fraction2.numerator), fraction1.denominator)
        new_numerator = (fraction1.numerator // gcd1) * (fraction2.numerator // gcd2)
        new_denominator = (fraction1.denominator // gcd2) * (fraction2.denominator // gcd1)
        return FracMath.simplify(Fraction(new_numerator, new_denominator))

    @staticmethod
    def divide(fraction1: object, fraction2: object) -> Fraction:
        """Divide the first Fraction-compatible value by the second."""
        from fracpylib.fractionlib.fraction import Fraction

        fraction1 = FracMath.as_fraction(fraction1)
        fraction2 = FracMath.as_fraction(fraction2)
        if fraction1 is NotImplemented or fraction2 is NotImplemented:
            return NotImplemented
        if fraction2.numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero.")

        gcd1 = math.gcd(abs(fraction1.numerator), abs(fraction2.numerator))
        gcd2 = math.gcd(fraction1.denominator, fraction2.denominator)
        new_numerator = (fraction1.numerator // gcd1) * (fraction2.denominator // gcd2)
        new_denominator = (fraction1.denominator // gcd2) * (fraction2.numerator // gcd1)
        return FracMath.simplify(Fraction(new_numerator, new_denominator))

    @staticmethod
    def mixedToNormal(whole: int, numerator: int, denominator: int) -> Fraction:
        """Convert a mixed fraction into an improper Fraction."""
        from fracpylib.fractionlib.fraction import Fraction

        for name, value in (
            ("whole", whole),
            ("numerator", numerator),
            ("denominator", denominator),
        ):
            if not isinstance(value, Integral) or isinstance(value, bool):
                raise TypeError(f"{name} must be an integer.")

        whole = int(whole)
        numerator = int(numerator)
        denominator = int(denominator)
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")
        if numerator < 0:
            raise ValueError("Mixed fraction numerator must be non-negative.")

        denominator = abs(denominator)
        if whole < 0:
            improper_numerator = (whole * denominator) - numerator
        elif whole > 0:
            improper_numerator = (whole * denominator) + numerator
        else:
            improper_numerator = numerator
        return FracMath.simplify(Fraction(improper_numerator, denominator))

    @staticmethod
    def from_periodic(whole: int = 0, non_repeating: str = "", repeating: str = "", sign: int = None) -> Fraction:
        """
        Convert a periodic decimal into a Fraction.

        Example: 1.1(6) -> whole=1, non_repeating="1", repeating="6" -> 7/6
        """
        from fracpylib.fractionlib.fraction import Fraction

        if not isinstance(whole, Integral) or isinstance(whole, bool):
            raise TypeError("Whole part must be an integer.")
        if sign is not None and sign not in (-1, 1):
            raise ValueError("Sign must be 1, -1, or None.")

        whole = int(whole)
        negative = whole < 0 if sign is None else sign < 0
        whole = abs(whole)
        non_repeating = FracMath._clean_decimal_digits(non_repeating, "non_repeating", allow_empty=True)
        repeating = FracMath._clean_decimal_digits(repeating, "repeating", allow_empty=True)

        if repeating:
            non_value = int(non_repeating) if non_repeating else 0
            combined_value = int((non_repeating or "0") + repeating)
            numerator = combined_value - non_value
            denominator = (10 ** len(non_repeating)) * ((10 ** len(repeating)) - 1)
            fractional = Fraction(numerator, denominator)
        elif non_repeating:
            fractional = Fraction(int(non_repeating), 10 ** len(non_repeating))
        else:
            fractional = Fraction(0, 1)

        result = FracMath.add(Fraction(whole, 1), fractional)
        return -result if negative else result

    @staticmethod
    def from_decimal(value: object) -> Fraction:
        """Convert an int, finite decimal string, Decimal, float, or periodic string to a Fraction."""
        from fracpylib.fractionlib.fraction import Fraction

        fraction = FracMath.as_fraction(value)
        if fraction is not NotImplemented:
            return fraction
        if isinstance(value, Decimal):
            return FracMath._from_decimal_object(value)
        if isinstance(value, float):
            if not math.isfinite(value):
                raise ValueError("Cannot convert an infinite or NaN float.")
            return FracMath._from_decimal_object(Decimal(str(value)))
        if isinstance(value, str):
            text = value.strip()
            if "(" in text or ")" in text:
                return FracMath._from_periodic_string(text)
            try:
                return FracMath._from_decimal_object(Decimal(text))
            except InvalidOperation as exc:
                raise ValueError(f"Invalid decimal string: {value!r}") from exc

        raise TypeError("Expected a Fraction, MixedFraction, int, float, Decimal, or decimal string.")

    @staticmethod
    def to_periodic(fraction: object) -> str:
        """Render a Fraction as a finite or periodic decimal string."""
        fraction = FracMath.as_fraction(fraction)
        if fraction is NotImplemented:
            raise TypeError("Expected a Fraction-compatible value.")

        if fraction.numerator == 0:
            return "0"

        sign = "-" if fraction.numerator < 0 else ""
        numerator = abs(fraction.numerator)
        denominator = fraction.denominator
        whole, remainder = divmod(numerator, denominator)
        if remainder == 0:
            return f"{sign}{whole}"

        digits = []
        seen_remainders = {}
        while remainder and remainder not in seen_remainders:
            seen_remainders[remainder] = len(digits)
            remainder *= 10
            digit, remainder = divmod(remainder, denominator)
            digits.append(str(digit))

        if remainder == 0:
            return f"{sign}{whole}.{''.join(digits)}"

        repeat_at = seen_remainders[remainder]
        non_repeating = "".join(digits[:repeat_at])
        repeating = "".join(digits[repeat_at:])
        return f"{sign}{whole}.{non_repeating}({repeating})"

    @staticmethod
    def _clean_decimal_digits(value: str, name: str, allow_empty: bool) -> str:
        if value is None:
            value = ""
        value = str(value).strip()
        if value == "" and allow_empty:
            return ""
        if not value.isdigit():
            raise ValueError(f"{name} must contain only decimal digits.")
        return value

    @staticmethod
    def _from_decimal_object(value: Decimal) -> Fraction:
        from fracpylib.fractionlib.fraction import Fraction

        if not value.is_finite():
            raise ValueError("Cannot convert an infinite or NaN decimal.")

        sign, digits, exponent = value.as_tuple()
        numerator = 0
        for digit in digits:
            numerator = (numerator * 10) + digit

        if exponent >= 0:
            numerator *= 10 ** exponent
            denominator = 1
        else:
            denominator = 10 ** (-exponent)

        if sign:
            numerator = -numerator
        return Fraction(numerator, denominator)

    @staticmethod
    def _from_periodic_string(value: str) -> Fraction:
        if value.count("(") != 1 or value.count(")") != 1 or not value.endswith(")"):
            raise ValueError(f"Invalid periodic decimal string: {value!r}")

        sign = -1 if value.startswith("-") else 1
        if value[:1] in ("-", "+"):
            value = value[1:]

        prefix, repeating = value[:-1].split("(", 1)
        if prefix == "":
            raise ValueError("Periodic decimal must include a whole or decimal point prefix.")
        if "." in prefix:
            whole, non_repeating = prefix.split(".", 1)
        else:
            whole, non_repeating = prefix, ""
        if whole and not whole.isdigit():
            raise ValueError("Whole part must contain only decimal digits.")

        return FracMath.from_periodic(
            whole=int(whole or "0"),
            non_repeating=non_repeating,
            repeating=repeating,
            sign=sign,
        )

    @staticmethod
    def getResultOfMul(fraction: object) -> int:
        fraction = FracMath.as_fraction(fraction)
        if fraction is NotImplemented:
            raise TypeError("Expected a Fraction-compatible value.")
        return fraction.denominator * fraction.numerator

    @staticmethod
    def getResultOfDiv(fraction: object) -> float:
        fraction = FracMath.as_fraction(fraction)
        if fraction is NotImplemented:
            raise TypeError("Expected a Fraction-compatible value.")
        return fraction.numerator / fraction.denominator
