from libs.Helper import get_exif, read_config, contype
from libs.ImageProcessing import resize_aspectratio_width_height, default_image
import cv2

def thumbnail(imgnumpy,imgpillow,ext,name,w,h,a,q):
    exif, imgrotate = get_exif(imgpillow)
    if exif != None:
        imgpillow = imgrotate
        width, height = imgrotate.size
    else:
        width, height = imgpillow.size

    if not w and not h and not a:
        image = default_image(imgpillow)

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