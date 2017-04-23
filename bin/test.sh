#!/bin/bash

source venv/bin/activate &&
heroku local:run python3 -m unittest discover --buffer
