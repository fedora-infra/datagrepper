# http://stackoverflow.com/questions/8007176/500-error-without-anything-in-the-apache-logs
import logging
import os
import sys

import __main__


__main__.__requires__ = ["SQLAlchemy >= 0.7", "jinja2 >= 2.4"]
logging.basicConfig(stream=sys.stderr)

os.environ["DATAGREPPER_CONFIG"] = "/etc/datagrepper/datagrepper.cfg"

import datagrepper.app  # noqa: E402


application = datagrepper.app.app
# application.debug = True  # Nope.  Be careful!

# vim: set ft=python:
