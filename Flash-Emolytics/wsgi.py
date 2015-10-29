#!/usr/bin/python

from server.Emolytics import emolytics
from wsgiref.simple_server import make_server
from werkzeug.debug import DebuggedApplication

if __name__ == '__main__':
    application = DebuggedApplication(emolytics, True)
    httpd = make_server('0.0.0.0', 8051, application)
    httpd.serve_forever()
