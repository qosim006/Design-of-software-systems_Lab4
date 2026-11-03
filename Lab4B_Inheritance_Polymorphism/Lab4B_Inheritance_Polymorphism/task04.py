"""
Task 4 — The audit log that could be erased

Answers:
4.1 AuditLog is not safely substitutable for a normal list because callers
    must not edit or delete recorded entries. clear(), pop() and sort()
    can violate the append-only rule.
4.2 AuditLog uses composition and exposes only record(), len(), iteration
    and last().
4.3 A frozen dataclass makes each entry immutable.
4.4 Overriding selected list methods is fragile: other mutating methods
    would remain available. dir(list) includes many public operations.
"""

from dataclasses import dataclass
from collections.abc import Iterator


@dataclass(frozen=True)
class AuditEntry:
    user: str
    action: str


class AuditLog:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, user: str, action: str) -> None:
        self._entries.append(AuditEntry(user, action))

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[AuditEntry]:
        return iter(self._entries)

    def last(self, n: int) -> tuple[AuditEntry, ...]:
        if n < 0:
            raise ValueError("n cannot be negative")
        if n == 0:
            return ()
        return tuple(self._entries[-n:])


def test_audit_log_records_and_iterates():
    log = AuditLog()
    log.record("admin", "approve_loan#77")
    log.record("ali", "view_account")

    assert len(log) == 2
    assert [entry.user for entry in log] == ["admin", "ali"]


def test_last_returns_recent_entries():
    log = AuditLog()
    log.record("admin", "login")
    log.record("ali", "payment")
    log.record("vali", "logout")

    assert [entry.user for entry in log.last(2)] == ["ali", "vali"]
    assert log.last(0) == ()


def test_entry_is_immutable():
    import pytest
    log = AuditLog()
    log.record("admin", "login")
    with pytest.raises((AttributeError, TypeError)):
        log.last(1)[0].action = "changed"  # type: ignore[misc]


def test_log_does_not_expose_list_mutators():
    log = AuditLog()
    log.record("admin", "login")
    assert not hasattr(log, "clear")
    assert not hasattr(log, "pop")
    assert not hasattr(log, "sort")
