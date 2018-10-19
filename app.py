import falcon
from route import route

def run() -> falcon.API():
    return route()

