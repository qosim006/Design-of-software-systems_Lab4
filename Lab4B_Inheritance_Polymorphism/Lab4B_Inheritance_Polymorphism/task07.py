"""
Task 7 — Dollars added to sums

Answers:
7.1 Money is frozen so its value cannot change. order=True would compare
    fields lexicographically and could compare unlike currencies.
7.2 sum() starts with integer 0, so __radd__ accepts that initial value.
    This keeps sum(items) convenient and is suitable when the list contains
    one currency; mixed currencies still raise CurrencyMismatchError.
7.3 For an unsupported operand, __add__ and __eq__ return NotImplemented
    so Python can try the other operand's implementation.
7.4 Money * Money and Money / Money are not implemented because their
    meaning is not unambiguous for this value object.
"""

from dataclasses import dataclass
from typing import Any


class CurrencyMismatchError(ValueError):
    pass


@dataclass(frozen=True, eq=False)
class Money:
    amount: int
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.amount, int):
            raise TypeError("amount must be an integer in minor units")
        if len(self.currency) != 3 or not self.currency.isalpha():
            raise ValueError("currency must be a 3-letter code")
        object.__setattr__(self, "currency", self.currency.upper())

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"cannot combine {self.currency} and {other.currency}"
            )

    def __add__(self, other: Any):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other: Any):
        if other == 0:
            return self
        if not isinstance(other, Money):
            return NotImplemented
        return other + self

    def __mul__(self, quantity: Any):
        if not isinstance(quantity, int):
            return NotImplemented
        return Money(self.amount * quantity, self.currency)

    def __rmul__(self, quantity: Any):
        return self * quantity

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other: Any):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self.amount < other.amount

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))


def test_money_addition_and_currency_check():
    import pytest
    assert Money(500, "UZS") + Money(300, "UZS") == Money(800, "UZS")
    with pytest.raises(CurrencyMismatchError):
        _ = Money(100, "USD") + Money(1, "UZS")


def test_money_multiplication_both_directions():
    price = Money(500, "UZS")
    assert price * 3 == Money(1500, "UZS")
    assert 3 * price == Money(1500, "UZS")


def test_money_equality_and_ordering():
    assert Money(500, "UZS") == Money(500, "UZS")
    assert (Money(500, "UZS") == 500) is False
    assert Money(100, "UZS") < Money(200, "UZS")


def test_sum_and_hash():
    items = [Money(100, "UZS"), Money(200, "UZS")]
    assert sum(items) == Money(300, "UZS")
    assert {Money(5, "UZS"): "five"}[Money(5, "UZS")] == "five"


def test_comparing_different_currencies_fails():
    import pytest
    with pytest.raises(CurrencyMismatchError):
        _ = Money(100, "USD") > Money(1, "UZS")
