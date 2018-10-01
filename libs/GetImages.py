
import urllib
from PIL import Image
import requests
from libs.Helper import strtodm5
import numpy as np
import cv2

def getimage(url):
    # imgNumpy
    urlfilter = urllib.parse.quote(url, ':/')
    img = urllib.request.Request(urlfilter)
    img.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36')
    resp = urllib.request.urlopen(img)
    imgNumpy = np.asarray(bytearray(resp.read()), dtype="uint8")

    # imgPillow
    imgPillow = Image.open(requests.get(urlfilter, stream=True).raw)

    # getextention
    ext = requests.head(urlfilter).headers
    extget = ext.get('Content-Type').split("/")[-1]
    type = {"jpeg": ".jpg",
            "png": ".png",
            "gif": ".gif",
            "x-icon": ".ico"}

    if type[extget] == ".png":
        imgNumpy = cv2.imdecode(imgNumpy, cv2.IMREAD_UNCHANGED)
    else:
        imgNumpy = cv2.imdecode(imgNumpy, cv2.IMREAD_COLOR)

    # generate name
    name = strtodm5(url, encoding='utf-8') + type[extget]
    return imgNumpy, imgPillow, type[extget], name