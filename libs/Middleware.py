import falcon
from urllib.parse import urlparse
from libs.Helper import read_config
import json
from libs.Helper import jsonSerializer

class AuthMiddleware(object):
    def __init__(self, exempt_routes=None):
        self.exempt_routes = exempt_routes or []

    def process_resource(self, req, resp, resource, params):
        aclDomain = read_config("domain_acl", None)
        parse = urlparse(req.get_param('url'))
        domain = '{uri.netloc}'.format(uri=parse)

        if req.path == '/' and req.get_param('url') is None:
            return
        elif req.path == '/' and domain in aclDomain:
            return
        elif req.get_header('domain') in aclDomain:
            return
        else:
            description = ('Please register your domain before using this service!')
            raise falcon.HTTPUnauthorized('Unauthorized', description)

class JSONTranslator:

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
                'Empty request body. A valid JSON document is required.'
            )

        try:
            req.context['request'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(
                falcon.HTTP_753,
                'Malformed JSON. Could not decode the request body.'
                'The JSON was incorrect or not encoded as UTF-8.'
            )

    def process_response(self, req, resp, resource, req_succeeded):
        if 'response' not in resp.context:
            return

        resp.text = json.dumps(
            resp.context['response'],
            default=jsonSerializer,
            sort_keys=True,
            indent=2,
            separators=(',', ': ')
        )
