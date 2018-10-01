import cv2
from libs.Helper import flat
from PIL import Image
import numpy as np
from libs.Helper import read_config

def default_image(img):
    pilimg = img
    if img.mode == "RGBA":  # for transparent image
        background_color = (255, 255, 255, 0)
        pilc = pilimg.convert("RGBA")
        canvas = Image.new('RGBA', pilc.size, background_color)
        canvas.paste(pilc, pilc)
        imgdefault = cv2.cvtColor(np.array(canvas), cv2.COLOR_RGBA2BGRA)
    else:
        imgdefault = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)

    return imgdefault

def height_only(img,h,width,height):
    roih = float(h)
    heightScale = roih / float(height)
    newX, newY = float(width) * float(heightScale), float(height) * float(heightScale)
    cropped_img = cv2.resize(img, (int(newX), int(newY)))
    return cropped_img

def width_only(img,w,width,height):
    roiw = float(w)
    widthScale = roiw / float(width)
    newX, newY = float(width) * float(widthScale), float(height) * float(widthScale)
    cropped_img = cv2.resize(img, (int(newX), int(newY)))
    return cropped_img

def resize_aspectratio_width_height(img, height, width, reqh, reqw):
    oriaspect = float(width) / float(height)
    reqaspect = float(reqw) / float(reqh)

    pilimg = img

    if reqaspect > oriaspect:
        scale_factor = float(reqw) / float(width)
        crop_size = (float(width), float(reqh) / scale_factor)
        top_cut_line = (float(height) - crop_size[1]) / 2

        pilimg = img.crop(flat
                          (0,  # left
                           top_cut_line,  # top
                           crop_size[0],  # right
                           top_cut_line + crop_size[1]  # bottom
                           )
                          )
    elif reqaspect < oriaspect:
        scale_factor = float(reqh) / float(height)
        crop_size = (float(reqw) / scale_factor, float(height))
        side_cut_line = (float(width) - crop_size[0]) / 2
        pilimg = img.crop(flat
                          (side_cut_line,
                           0,
                           side_cut_line + crop_size[0],
                           crop_size[1])
                          )

    if img.mode == "RGBA":  # for transparent image
        background_color = (255, 255, 255, 0)
        pilc = pilimg.convert("RGBA")
        canvas = Image.new('RGBA', pilc.size, background_color)
        canvas.paste(pilc, pilc)
        croped = canvas.resize((int(reqw), int(reqh)), Image.ANTIALIAS)
        cropped_img = cv2.cvtColor(np.array(croped), cv2.COLOR_RGBA2BGRA)

    else:
        croped = pilimg.resize((int(reqw), int(reqh)), Image.ANTIALIAS)
        cropped_img = cv2.cvtColor(np.array(croped), cv2.COLOR_RGB2BGR)

    return cropped_img

def resize_aspectratio_width_height_a(img, height, width, h, w, a):
    tocv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    if float(w) > float(h):
        roiw = float(w)
        widthScale = roiw / float(width)
        newX, newY = float(width) * float(widthScale), float(height) * float(widthScale)
    else:
        roiw = float(h)
        widthScale = roiw / float(height)
        newX, newY = float(width) * float(widthScale), float(height) * float(widthScale)

    dataprocess = cv2.resize(tocv, (int(newX), int(newY)))
    dataprocess = cv2.cvtColor(dataprocess, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(dataprocess)
    data = dataprocess

    if a == "t":
        top = pil_im.crop(
            (
                0,
                0,
                newX,
                int(h)
            )
        )

        data = cv2.cvtColor(np.array(top), cv2.COLOR_RGB2BGR)

    if a == "b":
        bottom = pil_im.crop(
            (
                0,
                int(newY) - int(h),
                newX,
                newY
            )
        )
        data = cv2.cvtColor(np.array(bottom), cv2.COLOR_RGB2BGR)

    if a == "l":
        left = pil_im.crop(
            (
                0,
                0,
                int(w),
                int(newY)
            )
        )
        data = cv2.cvtColor(np.array(left), cv2.COLOR_RGB2BGR)
    if a == "r":
        right = pil_im.crop(
            (
                int(newX) - int(w),
                0,
                newX,
                newY
            )
        )

        data = cv2.cvtColor(np.array(right), cv2.COLOR_RGB2BGR)

    return data

def crop_width_height(imgpil,position,height,width,h,w):
    crop = imgpil

    if position == "tl":
        crop = imgpil.crop((0, 0, int(w), int(h)))

    if position == "tr":
        crop = imgpil.crop(
            (
                width - int(w),
                0,
                width,
                int(h)
            )
        )

    if position == "br":
        crop = imgpil.crop(
            (
                width - int(w),
                height - int(h),
                width,
                height
            )
        )

    if position == "bl":
        crop = imgpil.crop(
            (
                0,
                height - int(h),
                int(w),
                height
            )
        )

    if position == "center":
        left = (width - int(w)) / 2
        top = (height - int(h)) / 2
        right = (width + int(w)) / 2
        bottom = (height + int(h)) / 2
        crop = imgpil.crop((left,top,right,bottom))


    cropped_img = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)
    return cropped_img

def flipimage(image):
    flip = cv2.flip(image, 1)
    return flip

def rotateimage(image,r):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, int(r), 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def overlayimage(signature,convertopil,o):

    wH, wW = signature.shape[:2]
    m, n = convertopil.shape[:2]

    (B, G, R, A) = cv2.split(signature)
    B = cv2.bitwise_and(B, B, mask=A)
    G = cv2.bitwise_and(G, G, mask=A)
    R = cv2.bitwise_and(R, R, mask=A)
    signature = cv2.merge([B, G, R, A])

    src = np.dstack([convertopil, np.ones((m, n), dtype="uint8") * 255])
    imgoverlay = np.zeros((m, n, 4), dtype="uint8")
    imgoverlay[m - wH - 10:m - 10, n - wW - 10:n - 10] = signature

    if o == "true":
        watermarked = src.copy()
        cv2.addWeighted(imgoverlay, 0.4, watermarked, 1.0, 0, watermarked)
        cv2.putText(watermarked, read_config('config','Overlay_Text'), (10, m - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=[255,255,255], thickness=1)
    elif o == "image":
        watermarked = src.copy()
        cv2.addWeighted(imgoverlay, 0.4, watermarked, 1.0, 0, watermarked)
    else:
        watermarked = src
        cv2.putText(watermarked, read_config('config','Overlay_Text'), (10, m - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=[255,255,255], thickness=1)

    return watermarked

def facecrop_debug(face_cascade,eye_cascade,img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    return img

def facecrop_default(img,face_cascade):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    #margin between face image
    left = 10
    right = 10
    top = 2
    bottom = 2

    count = len(faces)
    y = 0
    h = 0
    x = 0
    w = 0

    if count == 0:
        return img
    elif count <= 1:
        for (x, y, w, h) in faces:
            print
            x, y, w, h
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img[y - top:y + h + bottom, x - left:x + w + right]
    else:
        x = 0
        x1 = []
        y1 = []
        w1 = []
        h1 = []
        while x < count:
            x1.append(faces[x][0])
            y1.append(faces[x][1])
            w1.append(faces[x][0] + faces[x][2])
            h1.append(faces[x][1] + faces[x][3])
            x = x + 1

        x = min(x1)
        y = min(y1)
        w = max(w1)
        h = max(h1)

        return img[y - top:h + bottom, x - left: w + right]
