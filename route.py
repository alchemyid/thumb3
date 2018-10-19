import falcon
from libs.Middleware import AuthMiddleware
from controllers.Thumbnail import thumbController
from controllers.Crop import cropController
from controllers.Flip import flipController
from controllers.Rotate import rotateController
from controllers.Overlay import overlayController
from controllers.FaceCroping import facecropController
from controllers.index import index


def handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.body = 'Not found'

def route() -> falcon.API:

    route_check = AuthMiddleware(
    exempt_routes=[
                    '/'
                  ]
    )

    api = falcon.API(middleware=[route_check])

    #default index page
    api.add_route('/', index())

    #undefine route
    api.add_sink(handle_404, '')

    api.add_route('/v1.0/thumb', thumbController())
    api.add_route('/v1.0/cropping', cropController())
    api.add_route('/v1.0/flip',flipController())
    api.add_route('/v1.0/rotate', rotateController())
    api.add_route('/v1.0/overlay', overlayController())
    api.add_route('/v1.0/facecrop', facecropController())

    return api