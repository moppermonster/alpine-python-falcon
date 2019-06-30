'''
Json middleware for Falcon

Source: https://eshlox.net/2017/08/02/falcon-framework-json-middleware-loads-dumps/
'''

import datetime
import decimal
import json
import falcon


def json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return str(obj)

    raise TypeError("Cannot serialize {!r} (type {})".format(obj, type(obj)))

class JSONTranslator:

    # def __init__(self):
    #     pass

    def process_request(self, req, resp):
        """
        req.stream corresponds to the WSGI wsgi.input environ variable,
        and allows you to read bytes from the request body.
        See also: PEP 3333
        """

        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTPBadRequest(
                "Empty request body. A valid JSON document is required."
            )

        try:
            req.context["request"] = json.loads(body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(
                falcon.HTTP_753,
                "Malformed JSON. Could not decode the request body."
                "The JSON was incorrect or not encoded as UTF-8."
            )

    def process_resource(self, req, resp, resource, params):
        fail = False
        uri = req.relative_uri
        addr = req.remote_addr
        agent = req.user_agent
        if "request" in req.context:
            request = str(req.context["request"])
        else:
            request = ""
            fail = True
        method = req.method
        if fail:
            raise falcon.HTTPBadRequest(
                "Empty request body. A valid JSON document is required."
            )

    def process_response(self, req, resp, resource, req_succeeded):
        if "response" not in resp.context:
            return

        resp.body = json.dumps(
            resp.context["response"],
            default=json_serializer
        )
