from fracmath import FracMath  
class Fraction:
    def __init__(self, numerator, denominator):
        if denominator == 0:
            raise ZeroDivisionError("denominator cannot be zero")

        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"

    def __eq__(self, other):
        if isinstance(other, Fraction):
            return (
                self.numerator * other.denominator
                == self.denominator * other.numerator
            )
        return NotImplemented

    def __float__(self):
        return self.numerator / self.denominator
    
    def __add__(self, other):
        # Call FracMath as an instance in case add is an instance method
        return FracMath().add(self, other)
    
    def __sub__(self, other):
        return FracMath().sub(self, other)
    
    def __mul__(self, other):
        return FracMath().multiply(self, other)
    
    def __truediv__(self, other):
        return FracMath().divide(self, other)
    
class MixedFraction:
    def __init__(self, whole, numerator, denominator):
        if denominator == 0:
            raise ZeroDivisionError("denominator cannot be zero")

        self.numerator = numerator
        self.denominator = denominator
        self.whole = whole
        self.converted = FracMath().mixedToNormal(self.whole, self.numerator, self.denominator)

    def __str__(self):
        return f"{self.numerator}/{self.denominator}, whole={self.whole}"

    def __repr__(self):
        return f"MixedFraction({self.numerator}, {self.denominator}, {self.whole})"

    def __eq__(self, other: object):
        if not isinstance(other, MixedFraction):
            return NotImplemented
            
        Frac1 = FracMath().mixedToNormal(self.whole, self.numerator, self.denominator)
        Frac2 = FracMath().mixedToNormal(other.whole, other.numerator, other.denominator)
        
        return Frac1 == Frac2

    def __float__(self):
        return FracMath().getResultOfDiv(self.converted)
    
    def __add__(self, other):
        if not isinstance(other, MixedFraction):
            return NotImplemented
        # Call FracMath as an instance in case add is an instance method
        return FracMath().add(self.converted, FracMath().mixedToNormal(other.whole, other.numerator, other.denominator))
    
    def __sub__(self, other):
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return FracMath().sub(self.converted, FracMath().mixedToNormal(other.whole, other.numerator, other.denominator))
    
    def __mul__(self, other):
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return FracMath().multiply(self.converted, FracMath().mixedToNormal(other.whole, other.numerator, self.denominator))
    
    def __truediv__(self, other):
        if not isinstance(other, MixedFraction):
            return NotImplemented
        return FracMath().divide(self.converted, FracMath().mixedToNormal(other.whole, self.numerator, self.denominator))