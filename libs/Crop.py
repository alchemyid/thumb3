from libs.Helper import get_exif, read_config, contype
from libs.ImageProcessing import default_image,crop_width_height
import cv2
import base64
from io import BytesIO
from PIL import Image
import numpy as np


def crop(imgnumpy,imgpillow,ext,name,w,h,c,q):
    exif, imgrotate = get_exif(imgpillow)
    if exif != None:
        imgpillow = imgrotate
        width, height = imgrotate.size
    else:
        width, height = imgpillow.size

    image = crop_width_height(imgpillow,c,height,width,h,w)

    if q is not None:
        _, buf = cv2.imencode(ext, image, [int(cv2.IMWRITE_JPEG_QUALITY), int(q)])
    else:
        _, buf = cv2.imencode(ext, image,[int(cv2.IMWRITE_JPEG_QUALITY), read_config('config','Default_Qjpg')])

    expire, ctype = contype(name)
    return buf.tostring(), expire, ctype
