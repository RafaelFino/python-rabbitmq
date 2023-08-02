#!/bin/bash
 curl -X POST -i http://localhost:5000/publish -d '{ "queueName": "default-queue", "message": "teste de envio de mensagem" }' -H 'Content-Type: application/json'