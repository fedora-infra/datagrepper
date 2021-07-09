import os


if not os.environ.get("DATAGREPPER_CONFIG"):
    os.environ["DATAGREPPER_CONFIG"] = "../devel/development.cfg"

from datagrepper.app import app


app.run()
