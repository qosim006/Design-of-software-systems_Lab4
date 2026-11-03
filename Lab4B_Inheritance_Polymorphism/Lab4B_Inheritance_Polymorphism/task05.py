"""
Task 5 — A promotion that broke the payroll history

Answers:
5.1 A person remains an employee after promotion; the role changes, not
    the identity of the employee.
5.2 Employee has a role, and each role calculates its own monthly pay.
5.3 change_role() replaces the current role without replacing Employee.
5.4 Employee has a role-history collection (composition). Each entry keeps
    the role and the date from which it became active.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


class Role(ABC):
    @abstractmethod
    def monthly_pay(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True)
class LecturerRole(Role):
    hours: int

    def monthly_pay(self) -> int:
        return self.hours * 120_000


@dataclass(frozen=True)
class HeadRole(Role):
    salary: int

    def monthly_pay(self) -> int:
        return self.salary + 3_000_000


@dataclass(frozen=True)
class RolePeriod:
    role: Role
    start_date: date


class Employee:
    def __init__(self, emp_id: int, name: str, role: Role,
                 start_date: date) -> None:
        self.emp_id = emp_id
        self.name = name
        self._role_history = [RolePeriod(role, start_date)]

    @property
    def role(self) -> Role:
        return self._role_history[-1].role

    @property
    def role_history(self) -> tuple[RolePeriod, ...]:
        return tuple(self._role_history)

    def change_role(self, new_role: Role, start_date: date) -> None:
        if start_date <= self._role_history[-1].start_date:
            raise ValueError("new role must start after the current role")
        self._role_history.append(RolePeriod(new_role, start_date))

    def monthly_pay(self) -> int:
        return self.role.monthly_pay()

    def role_on(self, on_date: date) -> Role:
        for period in reversed(self._role_history):
            if period.start_date <= on_date:
                return period.role
        raise ValueError("no role was recorded for this date")

    def monthly_pay_on(self, on_date: date) -> int:
        return self.role_on(on_date).monthly_pay()


def test_promotion_keeps_employee_identity():
    lecturer = LecturerRole(hours=100)
    employee = Employee(7, "Ali", lecturer, date(2026, 1, 1))
    same_employee = employee

    employee.change_role(HeadRole(salary=14_000_000), date(2026, 6, 1))

    assert employee is same_employee
    assert employee.emp_id == 7
    assert employee.monthly_pay() == 17_000_000


def test_payroll_can_use_previous_month_role():
    employee = Employee(7, "Ali", LecturerRole(100), date(2026, 1, 1))
    employee.change_role(HeadRole(14_000_000), date(2026, 6, 1))

    assert employee.monthly_pay_on(date(2026, 5, 31)) == 12_000_000
    assert employee.monthly_pay_on(date(2026, 6, 1)) == 17_000_000


def test_role_history_is_preserved():
    employee = Employee(7, "Ali", LecturerRole(100), date(2026, 1, 1))
    employee.change_role(HeadRole(14_000_000), date(2026, 6, 1))

    assert len(employee.role_history) == 2
    assert employee.role_history[0].start_date == date(2026, 1, 1)


def test_role_change_date_must_be_later():
    import pytest
    employee = Employee(7, "Ali", LecturerRole(100), date(2026, 1, 1))
    with pytest.raises(ValueError):
        employee.change_role(HeadRole(14_000_000), date(2026, 1, 1))
