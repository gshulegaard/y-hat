from tests import BaseTestCase


from y_hat import amortization as amort


class AmortizationTestCase(BaseTestCase):
    def test_calculate_payment(self):
        payment = amort.calculate_payment(
            100000.00, 5.000, 120, amort.Schedule.MONTHLY
        )
        assert payment == 1060.66

        payment = amort.calculate_payment(
            100000.00, 5.000, 60, amort.Schedule.MONTHLY
        )
        assert payment == 1887.12

        # TODO: Test other schedules

    def test_calculate_interest(self):
        interest = amort.calculate_interest(100000.00, 5.000)
        assert interest == 416.67

        interest = amort.calculate_interest(100000.00, 6)
        assert interest == 500


    def test_calculate_period(self):
        principal = 100000.00
        rate = 5.000
        amort.calculate_period(
            balance=principal,
            payment=amort.calculate_payment(
                principal, rate, 120, amort.Schedule.MONTHLY
            ),
            rate=rate
        )

    def test_calculate_schedule(self):
        periods = amort.calculate_schedule(
            100000.00,
            5.000,
            n=120
        )

        assert len(periods) == 120

        # period 1
        assert periods[0].principal_paid == 643.99
        assert periods[0].interest_paid == 416.67
        assert periods[0].payment == 1060.66
        assert periods[0].balance == 99356.01

        # period 2
        assert periods[1].principal_paid == 646.68
        assert periods[1].interest_paid == 413.98
        assert periods[1].payment == 1060.66
        assert periods[1].balance == 98709.33

        # period 115
        assert periods[-5].principal_paid == 1038.84
        assert periods[-5].interest_paid == 21.82
        assert periods[-5].payment == 1060.66
        assert periods[-5].balance == 4198.08  # 4198.06
        # There is a small amount of drift, which we sort of expect given my
        # eager rounding.

        # final period
        assert periods[-1].principal_paid == 1056.26  # 1055.50
        assert periods[-1].interest_paid == 4.40
        assert periods[-1].payment == 1059.92  # 1059.90
        assert periods[-1].balance == 0  # 4198.06

