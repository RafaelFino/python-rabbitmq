
import datetime
from datetime import datetime as dt
from flask import Flask, request, make_response
from http import HTTPStatus
from infra.mqconn import MQConnection

conn = MQConnection()
app = Flask(__name__)

app.run()

def GetHeaders():
    return {
        'Content-Type': 'application/json'        
    }

def GetResponse():
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
    return make_response(GetResponse(), HTTPStatus.OK, GetHeaders())

@app.route('/connect', methods=['POST'])
def connect():
    app.logger.info("Connecting to MQ...")

    req = request.get_json()

    if CheckParams(['user', 'passwd'], req) != True:
        return make_response(GetResponse(), HTTPStatus.UNPROCESSABLE_ENTITY, GetHeaders())

    if conn.Connect(req['user'], req['passwd']) != True:
        return make_response(GetResponse(), HTTPStatus.BAD_GATEWAY, GetHeaders())

    return make_response(GetResponse(), HTTPStatus.OK, GetHeaders())


@app.route('/close', methods=['POST'])
def close():
    app.logger.info("Closing connection to MQ...")

    if conn.Disconnect() != True:
        return make_response(GetResponse(), HTTPStatus.BAD_GATEWAY, GetHeaders())

    return make_response(GetResponse(), HTTPStatus.OK, GetHeaders())

@app.route('/declare', methods=['POST'])
def declare():
    app.logger.info("Declaring queue...")

    request = request.get_json()

    if CheckParams(['queueName'], request) != True:
        return make_response(GetResponse(), HTTPStatus.UNPROCESSABLE_ENTITY, GetHeaders())

    if conn.DeclareQueue(request['queueName']) != True:
        return make_response(GetResponse(), HTTPStatus.BAD_GATEWAY, GetHeaders())

    return make_response(GetResponse(), HTTPStatus.OK, GetHeaders())

@app.route('/publish', methods=['POST'])
def publish():
    app.logger.info("Publishing message...")

    request = request.get_json()

    if CheckParams(['queueName', 'message'], request) != True:
        return GetResponse(), HTTPStatus.UNPROCESSABLE_ENTITY
    
    if conn.connected != True:
        return make_response(GetResponse(), HTTPStatus.BAD_GATEWAY, GetHeaders())

    if conn.Publish(request['queueName'], request['message']) != True:
        return make_response(GetResponse(), HTTPStatus.INTERNAL_SERVER_ERROR, GetHeaders())

    return make_response(GetResponse(), HTTPStatus.OK, GetHeaders())