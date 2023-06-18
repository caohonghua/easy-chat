# encoding: utf-8
from websocket import socketio,app

if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0')