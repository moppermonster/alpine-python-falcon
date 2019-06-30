'''
alpine-python-falcon default app.py

You can use this file as a starting point for building your own services

This example assumes use of the built in JSONTranslator Falcon middleware

Find out more: https://github.com/nielsds/alpine-python-falcon
'''

import falcon
from middleware import JSONTranslator

class Default(object):
    '''Default example'''
    def on_get(self, req, resp):
        """
        Hello world
        """
        response = "This is the default response for the alpine-python-falcon container."
        resp.status = falcon.HTTP_200
        resp.context["response"] = {"default": response}

# Falcon
APP = falcon.API(middleware=[JSONTranslator()])

# Resource class instances
DEFAULT = Default()

# Falcon routes
APP.add_route("/", DEFAULT)
