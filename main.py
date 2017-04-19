#!/usr/bin/python
import bottle
import tagmanager
import cors

app = application = bottle.default_app()

if __name__ == '__main__':
    # ec2-35-165-105-166.us-west-2.compute.amazonaws.com
    # 127.0.0.1
    bottle.run(host = '0.0.0.0', port = 8000)
