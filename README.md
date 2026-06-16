# fracpylib

[![PyPI - Version](https://img.shields.io/pypi/v/fracpylib.svg)](https://pypi.org/project/fracpylib)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fracpylib.svg)](https://pypi.org/project/fracpylib)

`fracpylib` is a small, dependency-free Python library for exact fraction arithmetic, mixed fractions, and recurring decimal conversion.

It keeps fractions normalized, supports natural operators, and can round-trip values such as `1.1(6)` without losing precision to floats.

## Contents

- [Highlights](#highlights)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Fraction API](#fraction-api)
- [Mixed fractions](#mixed-fractions)
- [Periodic decimals](#periodic-decimals)
- [Utilities](#utilities)
- [Development](#development)
- [License](#license)

## Highlights

| Feature | Example |
| --- | --- |
| Canonical immutable fractions | `Fraction(6, -8)` becomes `Fraction(-3, 4)` |
| Integer-friendly operators | `1 + Fraction(1, 2) == Fraction(3, 2)` |
| Mixed fractions | `MixedFraction(1, 5, 4)` becomes `2 1/4` |
| Periodic decimal parsing | `Fraction.from_decimal("0.(09)") == Fraction(1, 11)` |
| Periodic decimal rendering | `Fraction(1, 6).to_periodic() == "0.1(6)"` |
| Decimal utility checks | `FracMisc.is_terminating(Fraction(1, 8))` |

## Installation

```console
pip install fracpylib
```

## Quick Start

```python
from fracpylib.fractionlib import Fraction, MixedFraction

a = Fraction(2, 4)
b = Fraction.from_decimal("1.1(6)")

print(a)          # 1/2
print(b)          # 7/6
print(a + b)      # 5/3
print(2 * a)      # 1
print(float(b))   # 1.1666666666666667

mixed = MixedFraction(1, 5, 4)
print(mixed)             # 2 1/4
print(mixed.to_fraction())  # 9/4
```

## Fraction API

`Fraction` stores every value in reduced form with a positive denominator. Values are immutable after construction, so equality, hashing, string output, and comparisons all use the same canonical representation.

```python
from fracpylib.fractionlib import Fraction

x = Fraction(4, 8)
y = Fraction(3, 4)

assert x.as_tuple() == (1, 2)
assert x + y == Fraction(5, 4)
assert x - 1 == Fraction(-1, 2)
assert x * y == Fraction(3, 8)
assert x / y == Fraction(2, 3)
assert x ** -2 == Fraction(4, 1)
```

Helpful methods:

```python
from fracpylib.fractionlib import Fraction, MixedFraction

half = Fraction(1, 2)

assert half.reciprocal() == Fraction(2, 1)
assert half.to_mixed() == MixedFraction(0, 1, 2)
assert half.to_periodic() == "0.5"
```

## Mixed Fractions

`MixedFraction` accepts whole, numerator, and denominator pieces, then normalizes itself through an improper `Fraction`. Pass the sign on the whole part and keep the fractional numerator non-negative.

```python
from fracpylib.fractionlib import Fraction, MixedFraction

mf = MixedFraction(1, 5, 4)

assert str(mf) == "2 1/4"
assert mf.to_fraction() == Fraction(9, 4)
assert mf + Fraction(1, 4) == Fraction(5, 2)
assert 3 - mf == Fraction(3, 4)
```

Negative values are normalized too:

```python
assert str(MixedFraction.from_fraction(Fraction(-3, 2))) == "-1 1/2"
assert str(MixedFraction.from_fraction(Fraction(-1, 2))) == "-1/2"
```

## Periodic Decimals

Use `Fraction.from_decimal()` when you already have a decimal string. Repeating digits go in parentheses.

```python
from decimal import Decimal
from fracpylib.fractionlib import Fraction

assert Fraction.from_decimal("0.(3)") == Fraction(1, 3)
assert Fraction.from_decimal("1.1(6)") == Fraction(7, 6)
assert Fraction.from_decimal("-0.1(6)") == Fraction(-1, 6)
assert Fraction.from_decimal(".125") == Fraction(1, 8)
assert Fraction.from_decimal(Decimal("1.20")) == Fraction(6, 5)
```

Use `Fraction.from_periodic()` when the whole, non-repeating, and repeating parts are already separated:

```python
assert Fraction.from_periodic(whole=1, non_repeating="1", repeating="6") == Fraction(7, 6)
assert Fraction.from_periodic(whole=0, non_repeating="1", repeating="6", sign=-1) == Fraction(-1, 6)
```

Render exact decimals with `to_periodic()`:

```python
assert Fraction(1, 2).to_periodic() == "0.5"
assert Fraction(1, 3).to_periodic() == "0.(3)"
assert Fraction(1, 6).to_periodic() == "0.1(6)"
assert Fraction(-22, 7).to_periodic() == "-3.(142857)"
```

## Utilities

`FracMath` exposes arithmetic helpers for users who prefer function calls over operators. `FracMisc` contains common fraction predicates.

```python
from fracpylib.fractionlib import Fraction, FracMath, FracMisc

assert FracMath.add(Fraction(1, 2), Fraction(1, 3)) == Fraction(5, 6)
assert FracMisc.is_proper(Fraction(2, 3)) is True
assert FracMisc.is_improper(Fraction(3, 2)) is True
assert FracMisc.is_terminating(Fraction(1, 8)) is True
assert FracMisc.has_repeating_decimal(Fraction(1, 3)) is True
```

The old camelCase utility names are still available:

```python
assert FracMisc.isProper(Fraction(2, 3)) is True
assert FracMisc.isImproper(Fraction(3, 2)) is True
```

## Development

Create or activate a virtual environment, then run:

```console
python -m pip install -e . pytest
python -m pytest -q
```

Build the package locally with:

```console
python -m build
```

## License

`fracpylib` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
