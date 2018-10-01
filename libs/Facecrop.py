from libs.Helper import get_exif,getbuffer,contype
from libs.ImageProcessing import default_image, facecrop_debug, facecrop_default, width_only, height_only, resize_aspectratio_width_height
import cv2
from PIL import Image
import numpy as np

def facecrop(imgnumpy,imgpillow,ext,name,w,h,face,q):
    exif, imgrotate = get_exif(imgpillow)

    if exif != None:
        img = imgrotate
        width, height = imgrotate.size
    else:
        img = imgpillow
        width, height = imgpillow.size

    img = default_image(img)
    face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_eye.xml")

    if face == 'debug':
         image = facecrop_debug(face_cascade,eye_cascade,img)
    elif int(face) == 1:
        imagecrop = facecrop_default(img,face_cascade)
        if w is None and h is None:
            image = imagecrop
        if w is not None and h is None:
            image = width_only(imagecrop, w, width, height)
        elif h is not None and w is None:
            image = height_only(imagecrop, h, width, height)
        elif w is not None and h is not None:
            #change from np.array to pil
            image = cv2.cvtColor(np.array(imagecrop),cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)

            exif, imgrotate = get_exif(image)
            if exif != None:
                img = imgrotate
                width, height = imgrotate.size
            else:
                img = image
                width, height = image.size

            image = resize_aspectratio_width_height(img, height, width, h, w)

    buf = getbuffer(ext, image, q)
    expire, ctype = contype(name)
    return buf.tostring(), expire, ctype

