import os

if not os.environ.get("DATAGREPPER_CONFIG"):
    os.environ["DATAGREPPER_CONFIG"] = '../development.cfg'

from datagrepper import app
app.run()
