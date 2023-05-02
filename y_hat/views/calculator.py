# -*- coding: utf-8 -*-
import sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import openapi

from y_hat import amortization as amort


class Calculator(HTTPMethodView):
    @openapi.definition(
        summary="Simpe calculate endpoint"
    )
    async def post(self, request: sanic.Request):
        schedule = [
            i.to_dict() for i in amort.calculate_schedule(**request.json)
        ]
        return json(schedule)
