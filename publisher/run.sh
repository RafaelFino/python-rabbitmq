#!/bin/bash
export FLASK_APP=app/main && export FLASK_DEBUG=1 && flask run --reload --host=0.0.0.0 --debugger