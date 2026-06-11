import math
from fracpylib.fractionlib.fraction import Fraction
import warnings

class FracMath:
    def __init__(self):
        pass

    
    
    def simplify(self, fraction: Fraction, Recurse: bool, Value: int):
        """Simplifies a fraction

        Args:
            fraction (Fraction): Fraction to simplify
            Recurse (bool): If it simplify until the lowest value possible.
            Value (int): (only if Recurse is False) The value to simplify the fraction with.
        """
        # i genuinely have no ̶f̶u̶c̶k̶i̶n̶g̶ (profanity 😱😱😱) idea what i did here T_T
        if Recurse == True:
            gcd = math.gcd(fraction.numerator, fraction.denominator)
            simplified_numerator = fraction.numerator // gcd
            simplified_denominator = fraction.denominator // gcd
            return Fraction(simplified_numerator, simplified_denominator)
        else:
            if (fraction.numerator % Value == 0) and (fraction.denominator % Value == 0):
                simplified_numerator = fraction.numerator // Value
                simplified_denominator = fraction.denominator // Value
                return Fraction(simplified_numerator, simplified_denominator)
            else:
                print("THE VALUE MUST BE A COMMON DIVISOR OF THE NUMERATOR AND DENOMINATOR, DUMMY!")
                raise ValueError

    def amplify(self, fraction: Fraction, Value: int):
        """Amplifies a fraction with an given number

        Args:
            fraction (Fraction): The fraction to amplify
            Value (int): The value to amplify the fraction.

        Returns:
            Fraction: The amplified fraction.
        """
        return Fraction(fraction.numerator * Value, fraction.denominator * Value)

    def add(self, fraction1: Fraction, fraction2: Fraction):
        denominatorResult = 0
        """Adds 2 fractions

        Args:
            fraction1 (Fraction): Fraction to add 1
            fraction2 (Fraction): Fraction to add 2

        Returns:
            Fraction: The sum of the 2 fractions(of their numerators. Note they must have the same denominator)
        """
        numeratorResult = (fraction1.numerator + fraction2.numerator) 
        dem1 = fraction1.denominator
        if (fraction1.denominator == fraction2.denominator):
            self.simplify(Fraction(numerator=numeratorResult, denominator=dem1), Recurse=True, Value=0)
            denominatorResult = dem1
        else:
            print("BOTH OF THE DENOMINATORS MUST BE EQUAL!")
            raise ValueError
        return Fraction(numerator=numeratorResult, denominator=denominatorResult)
    
    def sub(self, fraction1: Fraction, fraction2: Fraction):
        denominatorResult = 0
        """Substracts 2 fractions

        Args:
            fraction1 (Fraction): Fraction to substract 1
            fraction2 (Fraction): Fraction to substract 2

        Returns:
            Fraction: The substraction of the 2 fractions(of their numerators. Note they must have the same denominator)
        """
        numeratorResult = (fraction1.numerator - fraction2.numerator) 
        dem1 = fraction1.denominator
        if (fraction1.denominator == fraction2.denominator):
            self.simplify(Fraction(numerator=numeratorResult, denominator=dem1), Recurse=True, Value=0)
            denominatorResult = dem1
        else:
            warnings.warn("The DENOMINATORS ARE NOT EQUAL.")
        return Fraction(numerator=numeratorResult, denominator=denominatorResult)
