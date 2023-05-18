import json
import cv2
from hashlib import md5
from datetime import datetime, timedelta
from PIL import Image
from PIL.ExifTags import TAGS
import urllib
import numpy as np
import decimal



def jsonSerializer(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return str(obj)

    raise TypeError(
        'Cannot serialize {!r} (type {})'.format(obj, type(obj)))
    
def flat(*nums):
    return tuple(int(round(n)) for n in nums)

def read_config(json_node, string):
    with open('config.json') as json_data:
        if string is None:
            d = json.load(json_data)
            return d[json_node]
        else:
            d = json.load(json_data)
            return d[json_node][string]

def strtodm5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def contype(name):
    #get extention
    ext = name.split(".")[-1]
    #appent with content type
    type = {"jpg": "image/jpeg",
                 "png": "image/png",
                 "gif": "image/gif",
                 "ico": "image/x-icon"}


    expires = datetime.utcnow() + timedelta(days=(1))
    expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return expires, type[ext]


def get_exif(fn):
    try:
        ret = {}
        info = fn._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

        if ret['Orientation'] == 1:
            return ret, fn
        if ret['Orientation'] == 2:
            return ret, fn.transpose(Image.FLIP_LEFT_RIGHT)
        elif ret['Orientation'] == 3:
            return ret, fn.transpose(Image.ROTATE_180)
        elif ret['Orientation'] == 4:
            return ret, fn.transpose(Image.FLIP_TOP_BOTTOM)
        elif ret['Orientation'] == 5:
            return ret, fn.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_90)
        elif ret['Orientation'] == 6:
            return ret, fn.transpose(Image.ROTATE_270)
        elif ret['Orientation'] == 7:
            return ret, fn.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
        elif ret['Orientation'] == 8:
            return ret, fn.transpose(Image.ROTATE_90)
    except:
        pass

    return None, None

def getbuffer(ext,image,q):

    if ext == ".jpg" or ext == ".jpeg":
        if q is not None:
            _, buf = cv2.imencode(ext, image, [int(cv2.IMWRITE_JPEG_QUALITY), int(q)])
        else:
            _, buf = cv2.imencode(ext, image,[int(cv2.IMWRITE_JPEG_QUALITY), read_config('config','Default_Qjpg')])
    elif ext == ".png":
        if q is not None:
            _, buf = cv2.imencode(ext, image, [int(cv2.IMWRITE_PNG_COMPRESSION), int(q)])
        else:
            _, buf = cv2.imencode(ext, image, [int(cv2.IMWRITE_PNG_COMPRESSION), read_config('config','Default_Cpng')])
    else:
        _, buf = cv2.imencode(ext, image)

    return buf


def getImageOverlay(url):

    urlfilter = urllib.parse.quote(url, ':/')
    img = urllib.request.Request(urlfilter)
    img.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36')
    resp = urllib.request.urlopen(img)
    SignatureNumpy = np.asarray(bytearray(resp.read()), dtype="uint8")

    image = cv2.imdecode(SignatureNumpy, cv2.IMREAD_UNCHANGED)
    return image