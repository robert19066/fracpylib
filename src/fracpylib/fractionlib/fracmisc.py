"""Class for other (misc) functions"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fracpylib.fractionlib.fraction import Fraction

class FracMisc:
    
    @staticmethod
    def is_power_of_10(n: int) -> bool:
        """Checks if a number is a power of 10."""
        if n <= 0:
            return False
        while n > 1:
            if n % 10 != 0:
                return False
            n //= 10
        return True

    @staticmethod
    def isProper(frac: Fraction) -> bool:
        """Returns True if the absolute value of the numerator is strictly less than the denominator."""
        return abs(frac.numerator) < abs(frac.denominator)
    
    @staticmethod
    def isImproper(frac: Fraction) -> bool:
        """Returns True if the absolute value of the numerator is greater than or equal to the denominator."""
        return abs(frac.numerator) >= abs(frac.denominator)