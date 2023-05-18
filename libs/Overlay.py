from libs.imageProcessing import resize_aspectratio_width_height,default_image,width_only,height_only,overlayimage
from libs.Helper import get_exif,getbuffer,getImageOverlay,read_config,contype
from libs.GetImages import getimage
import cv2
import numpy as np

def overlay(imgnumpy, imgpillow, ext, name, w, h, o, q):
    exif, imgrotate = get_exif(imgpillow)
    if exif != None:
        imgpillow = imgrotate
        width, height = imgrotate.size
    else:
        width, height = imgpillow.size

    convertopil = default_image(imgpillow)

    #resize overlay image
    signumpy, sigpillow, sigext, signame = getimage(read_config('config','Overlay_Image'))
    sigexif, sigimgrotate = get_exif(sigpillow)

    if sigexif != None:
        sigpillow = sigimgrotate
        sigwidth, sigheight = sigimgrotate.size
    else:
        sigwidth, sigheight = sigpillow.size

    signature = resize_aspectratio_width_height(sigpillow,sigheight,sigwidth,read_config('config','Overlay_Image_Width'),read_config('config','Overlay_Image_Height'))

    watermarked = overlayimage(signature,convertopil,o)

    if w is None and h is None:
        image = watermarked
    if w is not None and h is None:
        image = width_only(watermarked, w, width, height)
    elif h is not None and w is None:
        image = height_only(watermarked, h, width, height)
    elif w is not None and h is not None:
        image = overlayimage(signature,resize_aspectratio_width_height(imgpillow, height, width, h, w),o)

    buf = getbuffer(ext,image,q)
    expire, ctype = contype(name)
    return buf.tostring(),expire,ctype