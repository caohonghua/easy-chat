# encoding: utf-8
from flask import (Flask, request)
from flask_socketio import SocketIO
from .ws_utils import get_chain,ChatCallbackHandler
from logger import log

async_mode = 'gevent'
app = Flask(__name__)

socketio = SocketIO(app=app,async_mode=async_mode, logger=False,engineio_logger=False, cors_allowed_origins='*', transport='websocket')
app.socket_cache={}

@socketio.on('connect', namespace='/websocket')
def connect():
    user_id = request.args.get('user_id')
    client_ip = request.remote_addr
    user_key = client_ip + '-' + user_id
    get_chain(user_key,app)
    log.info('websocket连接成功, 客户端: ' + user_key)


@socketio.on('disconnect', namespace='/websocket')
def disconnect():
    user_id = request.args.get('user_id')
    client_ip = request.remote_addr
    user_key = client_ip + '-' + user_id
    del app.socket_cache[user_key]
    log.info('websocket连接断开, 客户端: ' + user_key)


@socketio.on('message', namespace='/websocket')
def message(data):
    log.info('received msg: ' + data)
    user_id = request.args.get('user_id')
    client_ip = request.remote_addr
    user_key = client_ip + '-' + user_id
    chain = get_chain(user_key,app)
    chain.predict(input=data, callbacks=[ChatCallbackHandler()])
