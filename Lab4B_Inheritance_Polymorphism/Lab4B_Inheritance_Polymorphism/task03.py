"""
Task 3 — Students charged without VAT

Answers:
3.1 FamilySubscription.__init__ must call super().__init__(user, months).
    The missing attributes are first accessed by price(), so construction
    itself does not raise an error.
3.2 Children override net(); price() applies VAT once in the parent.
3.3 Tests cover standard, student and family prices.
3.4 VAT is stored in Subscription.VAT_PERCENT, so only that class needs
    to be changed.
"""


class Subscription:
    VAT_PERCENT = 12

    def __init__(self, user: str, months: int) -> None:
        self.user = user
        self.months = months
        self.base_monthly = 50_000

    def net(self) -> int:
        return self.base_monthly * self.months

    def price(self) -> int:
        return self.net() * (100 + self.VAT_PERCENT) // 100


class StudentSubscription(Subscription):
    def net(self) -> int:
        return super().net() // 2


class FamilySubscription(Subscription):
    def __init__(self, user: str, months: int, members: int) -> None:
        super().__init__(user, months)
        if members < 1:
            raise ValueError("a family subscription needs at least one member")
        self.members = members

    def net(self) -> int:
        extra = 20_000 * (self.members - 1) * self.months
        return super().net() + extra


def test_standard_subscription_price():
    assert Subscription("Ali", 3).price() == 168_000


def test_student_subscription_price():
    assert StudentSubscription("Ali", 3).price() == 84_000


def test_family_subscription_price():
    # 150,000 base + 180,000 for three extra members; then 12% VAT.
    assert FamilySubscription("Ali", 3, 4).price() == 369_600


def test_vat_is_applied_in_one_place():
    original = Subscription.VAT_PERCENT
    try:
        Subscription.VAT_PERCENT = 15
        assert Subscription("Ali", 3).price() == 172_500
        assert StudentSubscription("Ali", 3).price() == 86_250
    finally:
        Subscription.VAT_PERCENT = original
