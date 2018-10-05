import json
import falcon
from libs.Crop import crop
from libs.GetImages import getimage

class cropController(object):
    def on_post(self, req, resp):
        try:
            rawjson = req.stream.read()
            data = json.loads(rawjson, encoding='utf-8')
            url = data['url']

            if url is None :
                urlempty = {"alert":"url image is mandatory"}
                resp.status = falcon.HTTP_503
                resp.body = json.dumps(urlempty, sort_keys=True, indent=2, separators=(',', ': '))
            else:

                if bool(data.get('width')) is False:
                    w = None
                else:
                    w = data['width']
                if bool(data.get('height')) is False:
                    h = None
                else:
                    h = data['height']
                if bool(data.get('crop')) is False:
                    c = None
                else:
                    c = data['crop']
                if bool(data.get('quality')) is False:
                    q = None
                else:
                    q = data['quality']

                #default get image to numpy and pillow
                imgnumpy,imgpillow,ext,name = getimage(url)

                buf, exp, ext = crop(imgnumpy, imgpillow, ext, name, w, h, c, q)
                resp.status = falcon.HTTP_200
                resp.content_type = ext
                resp.set_header("Expires", exp)
                resp.set_header("Cache-Control", "public, max-age=86400")
                resp.body = buf

        except :
            data = {
                "exec":False,
                "message":"url image is mandatory!"
            }
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))