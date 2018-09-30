from libs.Helper import get_exif, contype, getbuffer
from libs.ImageProcessing import default_image, flipimage,width_only,height_only,resize_aspectratio_width_height

def flip(imgnumpy,imgpillow,ext,name,w,h,f,q):

    if int(f) == 1:
        exif, imgrotate = get_exif(imgpillow)
        if exif != None:
            imgpillow = imgrotate
            width, height = imgrotate.size
        else:
            width, height = imgpillow.size

        convertopil = default_image(imgpillow)
        image = flipimage(convertopil)

        if w is not None and h is None:
            image = width_only(convertopil, w, width, height)
        elif h is not None and w is None:
            image = height_only(convertopil, h, width, height)
        elif w is not None and h is not None:
            image = resize_aspectratio_width_height(imgpillow, height, width, h, w)

        buf = getbuffer(ext, image, q)
        expire, ctype = contype(name)
        return buf.tostring(),expire,ctype
