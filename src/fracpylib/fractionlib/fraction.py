        
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