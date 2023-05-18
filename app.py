import falcon
from routes import routes
# from wsgiref import simple_server

def http() -> falcon.App():
    return routes()

# if __name__ == '__main__':
#     httpd = simple_server.make_server(
#             "0.0.0.0",
#             8000,
#             http()
#         )
#     httpd.serve_forever()