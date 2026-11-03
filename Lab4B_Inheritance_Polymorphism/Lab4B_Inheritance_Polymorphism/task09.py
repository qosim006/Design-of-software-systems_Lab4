"""
Task 9 — Invoices that were never saved

Answers:
9.1 MRO is TimestampMixin -> ValidateMixin -> AuditMixin -> Model.
    With the original ValidateMixin, the chain stops at validation.
9.2 Calling super().save() in ValidateMixin continues the chain. The audit
    entry appears after INSERT because AuditMixin calls super() first.
9.3 Invalid data should raise an exception. A silent return can make the
    API report success even though nothing was saved.
9.4 If Model comes before ValidateMixin, Model.save() ends the chain and
    validation is skipped. A cooperative base class should be last.
"""


class Model:
    def save(self) -> None:
        print("Model.save: INSERT/UPDATE")


class TimestampMixin:
    def save(self) -> None:
        print("TimestampMixin: set updated_at")
        super().save()


class ValidateMixin:
    def __init__(self, valid: bool = True) -> None:
        self.valid = valid

    def save(self) -> None:
        print("ValidateMixin: validate fields")
        if not self.valid:
            raise ValueError("invoice data is invalid")
        super().save()


class AuditMixin:
    def save(self) -> None:
        super().save()
        print("AuditMixin: write audit entry")


class Invoice(TimestampMixin, ValidateMixin, AuditMixin, Model):
    pass


class ReorderedInvoice(TimestampMixin, AuditMixin, Model, ValidateMixin):
    pass


def test_invoice_save_runs_all_steps(capsys):
    Invoice().save()
    output = capsys.readouterr().out.splitlines()
    assert output == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]


def test_invalid_invoice_stops_before_insert(capsys):
    import pytest
    invoice = Invoice()
    invoice.valid = False
    with pytest.raises(ValueError):
        invoice.save()
    output = capsys.readouterr().out.splitlines()
    assert output == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
    ]


def test_mro_places_model_last():
    assert Invoice.__mro__[:5] == (
        Invoice, TimestampMixin, ValidateMixin, AuditMixin, Model
    )


def test_reordered_bases_skip_validation(capsys):
    ReorderedInvoice().save()
    output = capsys.readouterr().out.splitlines()
    assert output == [
        "TimestampMixin: set updated_at",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]
