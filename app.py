import falcon
import json
from libs.Middleware import AuthMiddleware
from libs.imageProcessing import imageProcess

img = imageProcess()
class index(object):
    def on_get(self, req, resp):
        url = req.get_param('url')
        w = req.get_param('w')
        h = req.get_param('h')
        a = req.get_param('a')
        q = req.get_param('q')
        if url is None:
            data = {'status': 204,
                    'author': '@newbiemember',
                    'support':'info@girirahayu.com'
            }
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        else:
            imgNumpy,imgPillow,ext,name = img.getImage(url)
            buf,exp,ext = img.thumbnail(imgNumpy,imgPillow,ext,name,w,h,a,q)
            resp.status = falcon.HTTP_200
            resp.content_type = ext
            resp.set_header("Expires", exp)
            resp.set_header("Cache-Control", "public, max-age=86400")
            resp.body = buf

app = falcon.API(middleware=[AuthMiddleware()])
app.add_route('/', index())
