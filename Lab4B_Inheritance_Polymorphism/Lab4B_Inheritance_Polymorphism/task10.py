"""
Task 10 — Choosing the class from a string

Answers:
10.1 A single registry maps normalised names to payment-method classes.
10.2 UnknownPaymentMethodError includes the supported names.
10.3 Names are stripped and lower-cased once before lookup.
10.4 The mapping belongs at the system boundary where external strings are
     converted to objects. Checkout itself should work with the interface.
10.5 Adding BankTransfer requires adding its class to this registry only;
     Checkout does not change.
"""

from task01 import (
    PaymentMethod, Card, Click, Payme, Cash, BankTransfer
)


class UnknownPaymentMethodError(ValueError):
    pass


PAYMENT_METHODS: dict[str, type[PaymentMethod]] = {
    "card": Card,
    "click": Click,
    "payme": Payme,
    "cash": Cash,
    "bank_transfer": BankTransfer,
}


def create_payment_method(name: str) -> PaymentMethod:
    normalised_name = name.strip().lower()
    method_class = PAYMENT_METHODS.get(normalised_name)
    if method_class is None:
        supported = ", ".join(sorted(PAYMENT_METHODS))
        raise UnknownPaymentMethodError(
            f"unknown payment method '{name}'. Supported methods: {supported}"
        )
    return method_class()


def test_registry_creates_payment_methods():
    assert isinstance(create_payment_method("card"), Card)
    assert isinstance(create_payment_method("click"), Click)
    assert isinstance(create_payment_method("bank_transfer"), BankTransfer)


def test_name_is_normalised():
    assert isinstance(create_payment_method(" Payme "), Payme)
    assert isinstance(create_payment_method("PAYME"), Payme)
    assert isinstance(create_payment_method("payme"), Payme)


def test_unknown_name_lists_supported_methods():
    import pytest
    with pytest.raises(UnknownPaymentMethodError) as error:
        create_payment_method("crypto")
    assert "bank_transfer" in str(error.value)
    assert "click" in str(error.value)
