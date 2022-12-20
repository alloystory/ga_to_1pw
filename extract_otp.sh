#!/bin/bash

brew install zbar
brew install protobuf

poetry install
poetry run python extract_otp.py
