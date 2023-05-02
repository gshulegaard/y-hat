# -*- coding: utf-8 -*-
from tests import BaseTestCase

from y_hat.app import app


class CalculatorTestCase(BaseTestCase):
    def test_get(self):
        request, response = app.test_client.post(
            "/amortization/schedule",
            json={
                "initial_principal": 100000.00,
                "rate": 5.000,
                "n": 120
            }
        )

        assert request.method.lower() == "post"
        assert len(response.json) == 120
        assert response.status == 200
