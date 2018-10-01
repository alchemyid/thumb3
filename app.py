import falcon
import json
from libs.Middleware import AuthMiddleware
from libs.GetImages import getimage
from libs.Thumbnail import thumbnail
from libs.Crop import crop
from libs.Flip import flip
from libs.Rotate import rotate
from libs.Overlay import overlay

class index(object):
    def on_get(self, req, resp):
        url = req.get_param('url')
        w = req.get_param('w')
        h = req.get_param('h')
        a = req.get_param('a')
        q = req.get_param('q')
        c = req.get_param('c')
        f = req.get_param('f')
        r = req.get_param('r')
        o = req.get_param('o')
        if url is None:
            data = {'status': 204,
                    'author': '@newbiemember',
                    'support':'info@girirahayu.com'
            }
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        else:
            #default get image to numpy and pillow
            imgnumpy,imgpillow,ext,name = getimage(url)

            if c is not None:
                #crop
                buf,exp,ext = crop(imgnumpy,imgpillow,ext,name,w,h,c,q)
            elif f is not None:
                #flip
                buf,exp,ext = flip(imgnumpy,imgpillow,ext,name,w,h,f,q)
            elif r is not None:
                #rotate
                buf, exp, ext = rotate(imgnumpy,imgpillow,ext,name,w,h,r,q)
            elif o is not None:
                #overlay
                buf, exp, ext = overlay(imgnumpy, imgpillow, ext, name, w, h, o, q)
            else:
                #thumbnail
                buf, exp, ext = thumbnail(imgnumpy, imgpillow,ext,name,w,h,a,q)

            resp.status = falcon.HTTP_200
            resp.content_type = ext
            #resp.set_header("Expires", exp)
            #resp.set_header("Cache-Control", "public, max-age=86400")
            resp.body = buf


app = falcon.API(middleware=[AuthMiddleware()])
app.add_route('/', index())
