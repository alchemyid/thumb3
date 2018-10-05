import json
import falcon
from libs.GetImages import getimage
from libs.Thumbnail import thumbnail

class thumbController(object):
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
                if bool(data.get('alignment')) is False:
                    a = None
                else:
                    a = data['alignment']
                if bool(data.get('quality')) is False:
                    q = None
                else:
                    q = data['quality']

                #default get image to numpy and pillow
                imgnumpy,imgpillow,ext,name = getimage(url)

                buf, exp, ext = thumbnail(imgnumpy, imgpillow,ext,name,w,h,a,q)
                resp.status = falcon.HTTP_200
                resp.content_type = ext
                resp.set_header("Expires", exp)
                resp.set_header("Cache-Control", "public, max-age=86400")
                resp.body = buf

        except :
            data = {"exec":False}
            resp.status = falcon.HTTP_403
            resp.body = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))