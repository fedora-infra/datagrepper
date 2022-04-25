import argparse
import os


if not os.environ.get("DATAGREPPER_CONFIG"):
    os.environ["DATAGREPPER_CONFIG"] = "../devel/development.cfg"

from datagrepper.app import app  # isort:skip

parser = argparse.ArgumentParser(description="Run the Datagrepper app")


parser.add_argument(
    "--port", "-p", default=5000, help="Port for the flask application."
)

parser.add_argument(
    "--host",
    default="127.0.0.1",
    help="Hostname to listen on. When set to 0.0.0.0 the server is available \
    externally. Defaults to 127.0.0.1 making the it only visable on localhost",
)
args = parser.parse_args()
app.run(host=args.host, port=int(args.port))
