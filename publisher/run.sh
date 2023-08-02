#!/bin/bash
export FLASK_APP=src/main && export FLASK_DEBUG=1 && flask run --reload --host=0.0.0.0 --debugger