import urllib
import requests
import numpy as np
from PIL import Image

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
        return imgNumpy,imgPillow,type[extget]

    def thumbnail(self,imgNumpy,imgPillow,ext,w,h,a,q):
        print(ext)
