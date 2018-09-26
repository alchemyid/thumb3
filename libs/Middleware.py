import falcon
from urllib.parse import urlparse

class AuthMiddleware(object):

    def process_resource(self, req, resp, resource, params):


        aclDomain = [
            'cdn.netcj.co.id'
        ]

        parse = urlparse(req.get_param('url'))
        domain = '{uri.netloc}'.format(uri=parse)
        if req.path is '/' and req.get_param('url') is None:
            return
        elif req.path is '/' and domain in aclDomain:
            return
        else:
            description = ('Please register your domain before using this service!')
            raise falcon.HTTPUnauthorized('Unauthorized', description)
