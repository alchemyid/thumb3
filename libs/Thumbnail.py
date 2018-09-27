from libs.Helper import get_exif, read_config, contype
from libs.ImageProcessing import resize_aspectratio_width_height, default_image, width_only,height_only, \
    resize_aspectratio_width_height_a
import cv2

def thumbnail(imgnumpy,imgpillow,ext,name,w,h,a,q):
    exif, imgrotate = get_exif(imgpillow)
    if exif != None:
        imgpillow = imgrotate
        width, height = imgrotate.size
    else:
        width, height = imgpillow.size

    convertopil = default_image(imgpillow)

    if not w and not h and not a:
        image = convertopil
    elif w is not None and h is None:
        image = width_only(convertopil,w,width,height)
    elif h is not None and w is None:
        image = height_only(convertopil,h,width,height)
    elif w is not None and h is not None:
        image = resize_aspectratio_width_height(imgpillow,height,width,h,w)
        if a is not None:
            if int(w) > int(h):
                if a == "t" or a == "b":
                    image = resize_aspectratio_width_height_a(imgpillow, height, width, h, w, a)
                else:
                    image = resize_aspectratio_width_height(imgpillow, height, width, h, w)
            if int(h) > int(w):
                if a == "l" or a == "r":
                    image = resize_aspectratio_width_height_a(imgpillow, height, width, h, w, a)
                else:
                    image = resize_aspectratio_width_height(imgpillow, height, width, h, w)

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

    expire, ctype = contype(name)
    return buf.tostring(),expire,ctype