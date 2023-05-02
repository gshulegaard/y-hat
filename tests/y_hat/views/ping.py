# -*- coding: utf-8 -*-
from tests import BaseTestCase

from y_hat.app import app


class SanicHealthTestCase(BaseTestCase):
    def test_get(self):
        request, response = app.test_client.get("/ping")

        assert request.method.lower() == "get"
        assert response.json == {"response": "pong!"}
        assert response.status == 200
