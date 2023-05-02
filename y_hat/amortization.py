# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Schedule(Enum):
    YEARLY   = 1  # SIGQUIT
    MONTHLY  = 12  # SIGHUP


@dataclass
class PeriodData:
    rate: float
    schedule: Schedule
    payment: float
    principal_paid: float
    interest_paid: float
    balance: float

    @property
    def balance_before_payment(self):
        return round(self.balance + self.principal_paid, 2)

    def calculate_next_period(self):
        return calculate_period(
            balance=self.balance,
            payment=self.payment,
            rate=self.rate,
            schedule=self.schedule
        )

    def to_dict(self):
        return {
            "principal": self.principal_paid,
            "interest": self.interest_paid,
            "total_paid": self.payment,
            "balance": self.balance
        }


def calculate_payment(
    initial_principal: float,
    rate: float,
    n: int,
    schedule: Schedule = Schedule.MONTHLY
) -> float:
    """"
    Returns the payment size for a given load schedule.  The formula for this
    is:
        (i * P) / 1 - (1 + i)^-n

    :param initial_principal: float
        The starting value of the loan (in $).
    :param rate: float
        Interest rate as a percentage (e.g. 5% rate would be 5.00).  This is
        assumed to be an APR.
    :param n: int
        Number of payments.  For example, a 10-year loan, paid montly, would be
        120 payments.
    :param schedule: Schedule
        The payment schedule for the loan (e.g. paid monthly, yearly, etc.).
    :return: float
    """
    i = (rate / 100) / schedule.value  # i
    upper_value = i * initial_principal   # (i * P)
    lower_interest =  (1 + i) ** -abs(n)  # (1 + i)^-n
    payment = upper_value / (1 - lower_interest)
    return round(payment, 2)


def calculate_interest(
    principal: float,
    rate: float,
    schedule: Schedule = Schedule.MONTHLY
) -> float:
    """
    :param principal: float
        Principal remaining on the load in $.
    :param rate: float
        Interest rate as a percentage (e.g. 5% rate would be 5.00)
    :param schedule: Schedule
        The payment schedule for the loan (e.g. paid monthly, yearly, etc.).
    :return: float
        The amount paid in interest each payment.
    """
    i = (rate / 100) / schedule.value  # i
    interest = principal * i
    return round(interest, 2)


def calculate_period(
    balance: float,
    payment: float,
    rate: float,
    schedule: Schedule = Schedule.MONTHLY
) -> PeriodData:
    """
    :param balance: float
        Principal remaining on the load in $.
    :param payment: float
        The payment made for the period
    :param rate: float
        Interest rate as a percentage (e.g. 5% rate would be 5.00)
    :param schedule: Schedule
        The payment schedule for the loan (e.g. paid monthly, yearly, etc.).
    :return: PeriodData
    """
    interest_paid = calculate_interest(
        principal=balance,
        rate=rate,
        schedule=schedule
    )

    principal_paid = round(payment - interest_paid, 2)
    new_balance = round(float(balance - principal_paid), 2)
    return PeriodData(
        rate=rate,
        schedule=schedule,
        payment=payment if payment < balance else round(balance + interest_paid, 2),
        principal_paid=principal_paid,
        interest_paid=interest_paid,
        balance=new_balance if new_balance > 0 else 0
    )


def calculate_schedule(
    initial_principal: float,
    rate: float,
    n: int,
    schedule: Schedule = Schedule.MONTHLY
):
    payment = calculate_payment(
        initial_principal,
        rate,
        n,
        schedule
    )

    results = [
        calculate_period(
            balance=initial_principal,
            payment=payment,
            rate=rate,
            schedule=schedule
        )
    ]

    for _ in range(n-1):
        last_period = results[-1]
        results.append(
            last_period.calculate_next_period()
        )

    return results
