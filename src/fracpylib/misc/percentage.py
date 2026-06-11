from functools import total_ordering


@total_ordering
class Percentage:
    def __init__(self, value: float):
        self.value = float(value)

    def __str__(self) -> str:
        return f"{self.value * 100:g}%"

    def __repr__(self) -> str:
        return f"Percentage({self.value})"

    def __float__(self) -> float:
        return self.value

    def __int__(self) -> int:
        return int(self.value)

    def __hash__(self) -> int:
        return hash(round(self.value, 10))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Percentage):
            return round(self.value, 10) == round(other.value, 10)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Percentage):
            return self.value < other.value
        return NotImplemented

    @property
    def percent(self) -> float:
        """Returns 25 for 25%."""
        return self.value * 100

    @property
    def fraction(self) -> float:
        """Returns 0.25 for 25%."""
        return self.value

    @classmethod
    def from_percent(cls, value: float) -> "Percentage":
        return cls(value / 100)

    def as_percent(self) -> float:
        return self.value * 100

    def as_fraction(self) -> float:
        return self.value