from libs.imageProcessing import default_image,rotateimage,width_only,height_only,resize_aspectratio_width_height
from libs.Helper import getbuffer, get_exif,contype
import cv2

def rotate(imgnumpy,imgpillow,ext,name,w,h,r,q):

    if (type(int(r)) is int):
        exif, imgrotate = get_exif(imgpillow)
        if exif != None:
            imgpillow = imgrotate
            width, height = imgrotate.size
        else:
            width, height = imgpillow.size

        convertopil = default_image(imgpillow)

        if w is None and h is None:
            image = rotateimage(convertopil, r)
        if w is not None and h is None:
            image = width_only(rotateimage(convertopil, r), w, width, height)
        elif h is not None and w is None:
            image = height_only(rotateimage(convertopil, r), h, width, height)
        elif w is not None and h is not None:
            image = rotateimage(resize_aspectratio_width_height(imgpillow, height, width, h, w),r)

        buf = getbuffer(ext, image, q)

        expire, ctype = contype(name)
        return buf.tostring(), expire, ctype
