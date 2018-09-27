import json
import cv2
from hashlib import md5
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
from PIL.ExifTags import TAGS

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
