#!/bin/env python

from gevent import monkey
monkey.patch_all()

from grpc.experimental import gevent as grpc_gevent
grpc_gevent.init_gevent()

from app import create_app, socketio
import log
logger = log.setup_logger(__name__)


app = create_app(debug=False)
logger.info('应用启动成功')

if __name__ == '__main__':
    socketio.run(app)
    

