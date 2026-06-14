from __future__ import annotations
from fracmath import FracMath  

class Fraction:
    # __slots__ makes attribute access significantly faster and reduces memory overhead
    __slots__ = ('numerator', 'denominator')

    def __init__(self, numerator: int, denominator: int):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero, dummy!")
        
        # Keep the negative sign on the numerator for consistency
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        self.numerator = numerator
        self.denominator = denominator

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"

    # --- Math Operations ---
    def __add__(self, other: Fraction) -> Fraction:
        return FracMath.add(self, other)
    
    def __sub__(self, other: Fraction) -> Fraction:
        return FracMath.sub(self, other)
    
    def __mul__(self, other: Fraction) -> Fraction:
        return FracMath.multiply(self, other)
    
    def __truediv__(self, other: Fraction) -> Fraction:
        return FracMath.divide(self, other)
    
    def __abs__(self) -> Fraction:
        return Fraction(abs(self.numerator), abs(self.denominator))
        
    def __pow__(self, power: int) -> Fraction:
        return FracMath.simplify(Fraction(self.numerator ** power, self.denominator ** power))

    def __float__(self) -> float:
        return self.numerator / self.denominator

    # --- Rich Comparisons ---
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Fraction):
            return self.numerator * other.denominator == self.denominator * other.numerator
        return NotImplemented

    def __lt__(self, other: Fraction) -> bool:
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other: Fraction) -> bool:
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other: Fraction) -> bool:
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other: Fraction) -> bool:
        return self.numerator * other.denominator >= other.numerator * self.denominator


class MixedFraction:
    __slots__ = ('whole', 'numerator', 'denominator', 'converted')

    def __init__(self, whole: int, numerator: int, denominator: int):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero, dummy!")

        self.whole = whole
        self.numerator = numerator
        self.denominator = denominator
        self.converted = FracMath.mixedToNormal(self.whole, self.numerator, self.denominator)

    def __str__(self) -> str:
        return f"{self.whole} {self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        return f"MixedFraction({self.whole}, {self.numerator}, {self.denominator})"

    # --- Math Operations ---
    def __add__(self, other: object) -> Fraction:
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return FracMath.add(self.converted, other.converted)
    
    def __sub__(self, other: object) -> Fraction:
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return FracMath.sub(self.converted, other.converted)
    
    def __mul__(self, other: object) -> Fraction:
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return FracMath.multiply(self.converted, other.converted)
    
    def __truediv__(self, other: object) -> Fraction:
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return FracMath.divide(self.converted, other.converted)

    def __float__(self) -> float:
        return FracMath.getResultOfDiv(self.converted)

    # --- Rich Comparisons ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return self.converted == other.converted

    def __lt__(self, other: MixedFraction) -> bool:
        return self.converted < other.converted

    def __le__(self, other: MixedFraction) -> bool:
        return self.converted <= other.converted

    def __gt__(self, other: MixedFraction) -> bool:
        return self.converted > other.converted

    def __ge__(self, other: MixedFraction) -> bool:
        return self.converted >= other.converted