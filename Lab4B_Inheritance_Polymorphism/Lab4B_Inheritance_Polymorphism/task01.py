"""
Task 1 — A new payment method must not touch Checkout

Answers:
1.1 PaymentMethod is an abstract base class. Each payment defines fee() and
    whether its payments are refundable.
1.2 Click and Payme are separate classes. Their fees are equal today, but
    separate classes allow either provider's rule to change independently.
1.3 Checkout depends on the PaymentMethod interface, not provider names.
1.4 BankTransfer can be added without changing Checkout.
"""

from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def fee(self, amount: int) -> int:
        """Return the payment fee in sum."""
        raise NotImplementedError

    @property
    @abstractmethod
    def refundable(self) -> bool:
        raise NotImplementedError


class Card(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 15 // 1000

    @property
    def refundable(self) -> bool:
        return True


class Click(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000

    @property
    def refundable(self) -> bool:
        return True


class Payme(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000

    @property
    def refundable(self) -> bool:
        return True


class Cash(PaymentMethod):
    def fee(self, amount: int) -> int:
        return 0

    @property
    def refundable(self) -> bool:
        return False


class BankTransfer(PaymentMethod):
    def fee(self, amount: int) -> int:
        return 5_000

    @property
    def refundable(self) -> bool:
        return True


class Checkout:
    def pay(self, method: PaymentMethod, amount: int) -> dict:
        if amount < 0:
            raise ValueError("amount cannot be negative")
        return {
            "charged": amount + method.fee(amount),
            "refundable": method.refundable,
        }


def test_card_payment():
    assert Checkout().pay(Card(), 100_000) == {
        "charged": 101_500, "refundable": True
    }


def test_click_and_payme():
    checkout = Checkout()
    assert checkout.pay(Click(), 100_000)["charged"] == 101_000
    assert checkout.pay(Payme(), 100_000)["charged"] == 101_000


def test_cash_is_not_refundable():
    assert Checkout().pay(Cash(), 100_000) == {
        "charged": 100_000, "refundable": False
    }


def test_bank_transfer():
    assert Checkout().pay(BankTransfer(), 100_000) == {
        "charged": 105_000, "refundable": True
    }


def test_negative_amount_is_rejected():
    import pytest
    with pytest.raises(ValueError):
        Checkout().pay(Cash(), -1)
