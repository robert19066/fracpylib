from __future__ import annotations
import math
from typing import TYPE_CHECKING

# Prevent circular import loops at runtime
if TYPE_CHECKING:
    from fracpylib.fractionlib.fraction import Fraction

class FracMath:
    
    @staticmethod
    def simplify(fraction: Fraction, Recurse: bool = True, Value: int = 0) -> Fraction:
        """Simplifies a fraction to its lowest terms."""
        # Note: Importing Fraction here avoids circular dependencies during runtime initialization
        from fracpylib.fractionlib.fraction import Fraction 
        
        if Recurse:
            gcd = math.gcd(fraction.numerator, fraction.denominator)
            return Fraction(fraction.numerator // gcd, fraction.denominator // gcd)
        
        if Value == 0:
            raise ValueError("Cannot simplify with a value of 0.")
            
        if (fraction.numerator % Value == 0) and (fraction.denominator % Value == 0):
            return Fraction(fraction.numerator // Value, fraction.denominator // Value)
            
        raise ValueError(f"The value {Value} must be a common divisor, dummy!")

    @staticmethod
    def amplify(fraction: Fraction, Value: int) -> Fraction:
        """Amplifies a fraction with a given number."""
        from fracpylib.fractionlib.fraction import Fraction
        return Fraction(fraction.numerator * Value, fraction.denominator * Value)

    @staticmethod
    def add(fraction1: Fraction, fraction2: Fraction) -> Fraction:
        """Adds 2 fractions."""
        from fracpylib.fractionlib.fraction import Fraction
        new_numerator = (fraction1.numerator * fraction2.denominator) + (fraction2.numerator * fraction1.denominator)
        new_denominator = fraction1.denominator * fraction2.denominator
        return FracMath.simplify(Fraction(new_numerator, new_denominator))
    
    @staticmethod
    def sub(fraction1: Fraction, fraction2: Fraction) -> Fraction:
        """Subtracts 2 fractions."""
        from fracpylib.fractionlib.fraction import Fraction
        new_numerator = (fraction1.numerator * fraction2.denominator) - (fraction2.numerator * fraction1.denominator)
        new_denominator = fraction1.denominator * fraction2.denominator
        return FracMath.simplify(Fraction(new_numerator, new_denominator))

    @staticmethod
    def multiply(fraction1: Fraction, fraction2: Fraction) -> Fraction:
        """Multiplies two fractions."""
        from fracpylib.fractionlib.fraction import Fraction
        new_numerator = fraction1.numerator * fraction2.numerator
        new_denominator = fraction1.denominator * fraction2.denominator
        return FracMath.simplify(Fraction(new_numerator, new_denominator))

    @staticmethod
    def divide(fraction1: Fraction, fraction2: Fraction) -> Fraction:
        """Divides the first fraction by the second fraction."""
        from fracpylib.fractionlib.fraction import Fraction
        new_numerator = fraction1.numerator * fraction2.denominator
        new_denominator = fraction1.denominator * fraction2.numerator
        return FracMath.simplify(Fraction(new_numerator, new_denominator))
    
    @staticmethod
    def mixedToNormal(whole: int, numerator: int, denominator: int) -> Fraction:
        """Converts a mixed fraction into a regular (improper) Fraction."""
        from fracpylib.fractionlib.fraction import Fraction
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero, dummy!")

        improper_numerator = (whole * denominator) + numerator if whole >= 0 else (whole * denominator) - numerator
        return FracMath.simplify(Fraction(improper_numerator, denominator))

    @staticmethod
    def from_periodic(whole: int, non_repeating: str, repeating: str) -> Fraction:
        """
        Converts a periodic (repeating) decimal into a Fraction.
        Example: 0.1(6) -> whole=0, non_repeating="1", repeating="6" -> 1/6
        """
        from fracpylib.fractionlib.fraction import Fraction
        
        non_rep_str = non_repeating if non_repeating else "0"
        
        # Formula: (non_repeating + repeating) - (non_repeating) / (999...000...)
        num_part = int(non_rep_str + repeating) - int(non_rep_str)
        den_part = int(('9' * len(repeating)) + ('0' * len(non_repeating)))
        
        frac_part = Fraction(num_part, den_part)
        
        if whole == 0:
            return FracMath.simplify(frac_part)
            
        # Add the whole number part
        return FracMath.add(Fraction(whole, 1), frac_part)
    
    @staticmethod
    def getResultOfMul(fraction: Fraction) -> int:
        return fraction.denominator * fraction.numerator
    
    @staticmethod
    def getResultOfDiv(fraction: Fraction) -> float:
        return fraction.numerator / fraction.denominator