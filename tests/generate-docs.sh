#!/bin/bash
#
# Script to automatically build and test the Sphinx documentation currently in
# the repo. This script should always be run before submitting a new pull
# request.
# 
# If you're on Windows, please use the `make.bat` script in `docs/` directory.
#

cd ../datagrepper/docs/
make clean html

