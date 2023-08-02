
import datetime
from service.connection import MQConnection
from datetime import datetime as dt
from flask import Flask, request
from http import HTTPStatus

app = Flask(__name__)
conn = MQConnection()

def CreateStatusResponse():
    return {
        'connected': conn.connected,
        'timestamp': dt.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def CheckParams(targets, params) -> bool:
    for target in targets:
        if target not in params:
            return False
        
    return True

@app.route('/ping', methods=['GET'])
def pong():
    return {
        'timestamp': dt.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/status', methods=['GET'])
def status():
    app.logger.info("Checking MQ status...")
    return CreateStatusResponse(), HTTPStatus.OK

@app.route('/connect', methods=['POST'])
def connect():
    app.logger.info("Connecting to MQ...")

    req = request.get_json()

    if CheckParams(['user', 'passwd'], req) != True:
        return CreateStatusResponse(), HTTPStatus.UNPROCESSABLE_ENTITY

    if conn.Connect(req['user'], req['passwd']) != True:
        return CreateStatusResponse(), HTTPStatus.BAD_GATEWAY

    return CreateStatusResponse(), HTTPStatus.OK


@app.route('/close', methods=['POST'])
def close():
    app.logger.info("Closing connection to MQ...")

    ret = HTTPStatus.OK

    if conn.Disconnect() != True:
        ret = HTTPStatus.BAD_GATEWAY

    return CreateStatusResponse(), ret

@app.route('/declare', methods=['POST'])
def declare():
    app.logger.info("Declaring queue...")

    request = request.get_json()

    if CheckParams(['queueName'], request) != True:
        return CreateStatusResponse(), HTTPStatus.UNPROCESSABLE_ENTITY

    if conn.DeclareQueue(request['queueName']) != True:
        return CreateStatusResponse(), HTTPStatus.BAD_GATEWAY

    return CreateStatusResponse(), HTTPStatus.OK

@app.route('/publish', methods=['POST'])
def publish():
    app.logger.info("Publishing message...")

    request = request.get_json()

    if CheckParams(['queueName', 'message'], request) != True:
        return CreateStatusResponse(), HTTPStatus.UNPROCESSABLE_ENTITY
    
    if conn.connected != True:
        return CreateStatusResponse(), HTTPStatus.BAD_GATEWAY

    if conn.Publish(request['queueName'], request['message']) != True:
        return CreateStatusResponse(), HTTPStatus.INTERNAL_SERVER_ERROR

    return CreateStatusResponse(), HTTPStatus.OK    