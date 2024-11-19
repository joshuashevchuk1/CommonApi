#!/usr/bin/python

import api.app

def run_flask_app():
     server = api.app.CommonApp("9020")
     server.run_server()

if __name__ == '__main__':
    run_flask_app()