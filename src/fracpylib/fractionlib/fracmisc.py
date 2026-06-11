
"""Class for other(misc) functions"""
from fracpylib.fractionlib.fraction import Fraction
from fracpylib.misc.percentage import Percentage

class FracMisc:
    def __init__(self):
        pass
    
    def _is_power_of_10(self, n: int) -> bool:
        while n > 1:
            if n % 10 != 0:
                return False
            n //= 10
        return n == 1

    def isProper(self, frac: Fraction) -> bool:
        isTrue = False

        if (frac.denominator > frac.numerator):
            isTrue = True
        else:
            pass

        return isTrue
    
    def isImproper(self, frac: Fraction) -> bool:
        isTrue = False

        if (frac.denominator < frac.numerator):
            isTrue = True
        else:
            pass

        return isTrue
    
    def toPercentage(self, frac: Fraction) -> Percentage:
        if (self._is_power_of_10(frac.denominator)):
            return Percentage(frac.numerator / frac.denominator)
        else:
            raise ValueError("Denominator must be a power of 10")