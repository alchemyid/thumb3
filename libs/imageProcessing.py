import cv2
from libs.Helper import flat
from PIL import Image
import numpy as np

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

    if position == "top-left":
        crop = imgpil.crop((0, 0, int(w), int(h)))

    if position == "top-right":
        crop = imgpil.crop(
            (
                width - int(w),
                0,
                width,
                int(h)
            )
        )

    if position == "bottom-right":
        crop = imgpil.crop(
            (
                width - int(w),
                height - int(h),
                width,
                height
            )
        )

    if position == "bottom-left":
        crop = imgpil.crop(
            (
                0,
                height - int(h),
                width - int(w),
                height
            )
        )

    if position == "center":
        half_the_width = width / 2
        half_the_height = height / 2

        crop = imgpil.crop(
            (
                half_the_width - int(w),
                half_the_height - int(h),
                half_the_width + int(w),
                half_the_height + int(h)
            )
        )

    cropped_img = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)
    return cropped_img