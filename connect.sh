#!/bin/bash
curl -X POST -i http://localhost:5000/connect -d '{ "user": "user", "password": "password" }' -H 'Content-Type: application/json'