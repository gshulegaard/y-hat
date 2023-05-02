# -*- coding: utf-8 -*-
import sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import openapi


class Ping(HTTPMethodView):
    @openapi.definition(
        summary="Simpe ping endpoint",
        response=[openapi.definitions.Response(json("pong!"))]
    )
    async def get(self, request: sanic.Request):
        app = sanic.Sanic.get_app()
        app.ctx.log.debug("Hmm, we received a ping...")
        return json({"response": "pong!"})
