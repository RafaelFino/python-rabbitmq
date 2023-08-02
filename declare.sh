#!/bin/bash
 curl -X POST -i http://localhost:5000/declare -d '{ "queueName": "minhaFilona" }' -H 'Content-Type: application/json'