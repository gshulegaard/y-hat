# -*- coding: utf-8 -*-
from sanic import Sanic

from y_hat import __version__
from y_hat.context import context


context.app_name = "y-hat-api"


app = Sanic(
    context.app_name,
    ctx=context
)
# Apply Sanic configuration values from engin config
app.config.update(**context.config.get("server", {}))


## Update openapi meta
from textwrap import dedent
app.ext.openapi.describe(
    "y-hat API",
    version=__version__,
    description=dedent(
        """
        Not sure what this will do yet.
        """
    ),
)


## Add routes
from y_hat.views.ping import Ping
app.add_route(Ping.as_view(), "/ping")

from y_hat.views.calculator import Calculator
app.add_route(Calculator.as_view(), "/amortization/schedule")
