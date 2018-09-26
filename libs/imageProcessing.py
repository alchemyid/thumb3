import urllib
import requests
import numpy as np
import cv2
from hashlib import md5
from PIL import Image
from datetime import datetime, timedelta
from libs.globalFunctions import flat


def strtodm5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def contype(name):
    ext = name.split(".")[-1]
    type = {"jpg": "image/jpeg",
                 "png": "image/png",
                 "gif": "image/gif",
                 "ico": "image/x-icon"}


    expires = datetime.utcnow() + timedelta(days=(1))
    expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    #    web.header("Expires", expires)
    #    web.header("Cache-Control", "public, max-age=86400")
    #    web.header("Accept-Ranges", "bytes")
    #    web.header("Content-Type", self.type[self.ext])

    return expires, type[ext]


def resize_aspectratio_width_height(img, height, width, reqh, reqw, ext):
    oriaspect = float(width) / float(height)
    reqaspect = float(reqw) / float(reqh)

    pilimg = img

    if reqaspect > oriaspect:
        scale_factor = float(reqw) / float(width)
        crop_size = (float(width), float(reqh) / scale_factor)
        top_cut_line = (float(height) - crop_size[1]) / 2

        pilimg = img.crop(flat
                          (0,  # left
                           top_cut_line,  # top
                           crop_size[0],  # right
                           top_cut_line + crop_size[1]  # bottom
                           )
                          )
    elif reqaspect < oriaspect:
        scale_factor = float(reqh) / float(height)
        crop_size = (float(reqw) / scale_factor, float(height))
        side_cut_line = (float(width) - crop_size[0]) / 2
        pilimg = img.crop(flat
                          (side_cut_line,
                           0,
                           side_cut_line + crop_size[0],
                           crop_size[1])
                          )

    if img.mode == "RGBA":  # for transparent image
        background_color = (255, 255, 255, 0)
        pilc = pilimg.convert("RGBA")
        canvas = Image.new('RGBA', pilc.size, background_color)
        canvas.paste(pilc, pilc)
        croped = canvas.resize((int(reqw), int(reqh)), Image.ANTIALIAS)
        cropped_img = cv2.cvtColor(np.array(croped), cv2.COLOR_RGBA2BGRA)

    else:
        croped = pilimg.resize((int(reqw), int(reqh)), Image.ANTIALIAS)
        cropped_img = cv2.cvtColor(np.array(croped), cv2.COLOR_RGB2BGR)

    return cropped_img

class imageProcess(object):
    def getImage(self,url):
        #imgNumpy
        urlFilter = urllib.parse.quote(url, ':/')
        img = urllib.request.Request(urlFilter)
        img.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36')
        resp = urllib.request.urlopen(img)
        imgNumpy = np.asarray(bytearray(resp.read()), dtype="uint8")

        #imgPillow
        imgPillow = Image.open(requests.get(urlFilter, stream=True).raw)

        #getextention
        ext = requests.head(urlFilter).headers
        extget = ext.get('Content-Type').split("/")[-1]
        type = {"jpeg": ".jpg",
                "png": ".png",
                "gif": ".gif",
                "x-icon": ".ico"}

        #generate name
        name = strtodm5(url, encoding='utf-8') + type[extget]
        return imgNumpy,imgPillow,type[extget],name

    def thumbnail(self,imgNumpy,imgPillow,ext,name,w,h,a,q):
        width, height = imgPillow.size

        image = resize_aspectratio_width_height(imgPillow,height,width,h,w,ext)
        flag, buf = cv2.imencode(ext, image,[int(cv2.IMWRITE_JPEG_QUALITY), 80])
        exp, ctype = contype(name)
        return buf.tostring(),exp,ctype