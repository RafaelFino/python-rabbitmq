
import datetime
from datetime import datetime as dt
from flask import Flask, request, make_response
from http import HTTPStatus
from infra.mqconn import MQConnection
import logging
from flask.logging import default_handler

conn = MQConnection()
app = Flask(__name__)
                     
app.run()

def GetHeaders():
    return {
        'Content-Type': 'application/json'        
    }

def GetResponse(args = {}):
    ret = {
        'connected': conn.connected,
        'timestamp': dt.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    for i in args.keys():
        ret[i] = args[i]

    app.logger.info("Response: {}".format(ret))

    return ret

def CheckParams(targets, params) -> bool:
    for target in targets:
        if target not in params:
            return False
        
    return True

@app.route('/status', methods=['GET'])
def status():
    app.logger.info("/status -> Checking MQ status...")
    return make_response(GetResponse(), HTTPStatus.OK, GetHeaders())

@app.route('/connect', methods=['POST'])
def connect():
    app.logger.info("/connect -> Connecting to MQ...")

    req = request.get_json()

    if CheckParams(['user', 'password'], req) != True:
        return make_response(GetResponse({'return-message': "Missing arguments"} ), HTTPStatus.UNPROCESSABLE_ENTITY, GetHeaders())

    ret = None

    try:
       ret = conn.Connect(req['user'], req['password'])        
    except Exception as Err:
        return make_response(GetResponse({ 'return-message': str(ret), 'exception': str(Err) }), HTTPStatus.BAD_GATEWAY, GetHeaders())
    
    return make_response(GetResponse({ 'return-message': str(ret) }), HTTPStatus.OK, GetHeaders())


@app.route('/close', methods=['POST'])
def close():
    app.logger.info("/close -> Closing connection to MQ...")

    ret = None
    
    try:
        ret = conn.Disconnect()
    except Exception as Err:
        return make_response(GetResponse({ 'return-message': str(ret), 'exception': str(Err) }), HTTPStatus.BAD_GATEWAY, GetHeaders())
        
    return make_response(GetResponse({ 'return-message': str(ret) }), HTTPStatus.OK, GetHeaders())

@app.route('/declare', methods=['POST'])
def declare():
    app.logger.info("/declare -> Declaring queue...")    

    req = request.get_json()

    if CheckParams(['queueName'], req) != True:        
        return make_response(GetResponse({'return-message': "Missing arguments"} ), HTTPStatus.UNPROCESSABLE_ENTITY, GetHeaders())
    
    if conn.connected != True:
        return make_response(GetResponse(), HTTPStatus.BAD_GATEWAY, GetHeaders())    

    ret = None

    try:
        ret = conn.DeclareQueue(req['queueName'])
    except Exception as Err:
        return make_response(GetResponse({ 'return-message': str(ret), 'exception': str(Err) }), HTTPStatus.BAD_GATEWAY, GetHeaders())

    return make_response(GetResponse({ 'return-message': str(ret) }), HTTPStatus.OK, GetHeaders())

@app.route('/publish', methods=['POST'])
def publish():
    app.logger.info("/publish -> Publishing message...")

    req = request.get_json()

    if CheckParams(['queueName', 'message'], req) != True:        
        return make_response(GetResponse({'return-message': "Missing arguments"} ), HTTPStatus.UNPROCESSABLE_ENTITY, GetHeaders())
    
    if conn.connected != True:
        return make_response(GetResponse(), HTTPStatus.BAD_GATEWAY, GetHeaders())

    ret = None

    try:
        ret = conn.Send(req['queueName'], req['message'])        
    except Exception as Err:
        return make_response(GetResponse({ 'return-message': str(ret), 'exception': str(Err) }), HTTPStatus.INTERNAL_SERVER_ERROR, GetHeaders())
    
    return make_response(GetResponse({ 'return-message': str(ret) }), HTTPStatus.OK, GetHeaders())