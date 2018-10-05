import falcon
from urllib.parse import urlparse

class AuthMiddleware(object):
    def __init__(self, exempt_routes=None):
        self.exempt_routes = exempt_routes or []

    def process_resource(self, req, resp, resource, params):
        aclDomain = [
            'cdn.netcj.co.id',
            'raw.githubusercontent.com',
            'www.jcpportraits.com'
        ]
        parse = urlparse(req.get_param('url'))
        domain = '{uri.netloc}'.format(uri=parse)

        if req.path is '/' and req.get_param('url') is None:
            return
        elif req.path is '/' and domain in aclDomain:
            return
        elif req.get_header('domain') in aclDomain:
            return
        else:
            description = ('Please register your domain before using this service!')
            raise falcon.HTTPUnauthorized('Unauthorized', description)
