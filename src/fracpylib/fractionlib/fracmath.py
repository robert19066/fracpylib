import math
from fracpylib.fractionlib.fraction import Fraction
import warnings

class FracMath:
    def __init__(self):
        pass

    def simplify(self, fraction: Fraction, Recurse: bool, Value: int = 0):
        """Simplifies a fraction.

        Args:
            fraction (Fraction): Fraction to simplify
            Recurse (bool): If True, simplifies to the lowest value possible.
            Value (int): (only if Recurse is False) The value to simplify the fraction with.
        """
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
                raise ValueError("Not a common divisor.")

    def amplify(self, fraction: Fraction, Value: int):
        """Amplifies a fraction with a given number.

        Args:
            fraction (Fraction): The fraction to amplify
            Value (int): The value to amplify the fraction.

        Returns:
            Fraction: The amplified fraction.
        """
        return Fraction(fraction.numerator * Value, fraction.denominator * Value)

    def add(self, fraction1: Fraction, fraction2: Fraction):
        """Adds 2 fractions automatically by finding a common denominator.

        Args:
            fraction1 (Fraction): First fraction
            fraction2 (Fraction): Second fraction

        Returns:
            Fraction: The simplified sum of the 2 fractions.
        """
        # Cross-multiply to get a common denominator automatically!
        new_numerator = (fraction1.numerator * fraction2.denominator) + (fraction2.numerator * fraction1.denominator)
        new_denominator = fraction1.denominator * fraction2.denominator
        
        # Save and return the simplified result so it doesn't get thrown away
        raw_result = Fraction(numerator=new_numerator, denominator=new_denominator)
        return self.simplify(raw_result, Recurse=True)
    
    def sub(self, fraction1: Fraction, fraction2: Fraction):
        """Subtracts 2 fractions automatically by finding a common denominator.

        Args:
            fraction1 (Fraction): Fraction being subtracted from
            fraction2 (Fraction): Fraction to subtract

        Returns:
            Fraction: The simplified difference of the 2 fractions.
        """
        # Cross-multiply just like addition, but subtract
        new_numerator = (fraction1.numerator * fraction2.denominator) - (fraction2.numerator * fraction1.denominator)
        new_denominator = fraction1.denominator * fraction2.denominator
        
        raw_result = Fraction(numerator=new_numerator, denominator=new_denominator)
        return self.simplify(raw_result, Recurse=True)

    def multiply(self, fraction1: Fraction, fraction2: Fraction):
        """Multiplies two fractions.
        
        Args:
            fraction1 (Fraction): First fraction
            fraction2 (Fraction): Second fraction
            
        Returns:
            Fraction: The simplified product.
        """
        new_numerator = fraction1.numerator * fraction2.numerator
        new_denominator = fraction1.denominator * fraction2.denominator
        
        raw_result = Fraction(numerator=new_numerator, denominator=new_denominator)
        return self.simplify(raw_result, Recurse=True)

    def divide(self, fraction1: Fraction, fraction2: Fraction):
        """Divides the first fraction by the second fraction.
        
        Args:
            fraction1 (Fraction): The dividend
            fraction2 (Fraction): The divisor
            
        Returns:
            Fraction: The simplified quotient.
        """
        # To divide fractions, you multiply by the reciprocal (flip the second fraction)
        new_numerator = fraction1.numerator * fraction2.denominator
        new_denominator = fraction1.denominator * fraction2.numerator
        
        raw_result = Fraction(numerator=new_numerator, denominator=new_denominator)
        return self.simplify(raw_result, Recurse=True)