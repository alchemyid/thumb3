from libs.Helper import get_exif, contype, getbuffer
from libs.imageProcessing import crop_width_height

def crop(imgnumpy,imgpillow,ext,name,w,h,c,q):
    exif, imgrotate = get_exif(imgpillow)
    if exif != None:
        imgpillow = imgrotate
        width, height = imgrotate.size
    else:
        width, height = imgpillow.size

    image = crop_width_height(imgpillow,c,height,width,h,w)

    buf = getbuffer(ext, image, q)
    expire, ctype = contype(name)
    return buf.tostring(), expire, ctype
