from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops
import os
import sys
import urllib.request
import cairosvg
from io import BytesIO

def guide_ify(url):
    print(f"Image location: {url}")

    if ".jpg" in url:
        urllib.request.urlretrieve("https://" + url, "jpg_image.jpg")
        path = "jpg_image.jpg"
        jpg_flow(path)
        return path
    elif ".svg" in url:
        urllib.request.urlretrieve("https://" + url, "svg_image.svg")
        path = "svg_image.svg"
        out = BytesIO()
        cairosvg.svg2png(url=path, write_to=out)

        jpg_flow(out)
        return out
    else:
        return "default.jpg"

def resize(image, new_width=250):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)

    return new_image

def filters(image):

    image = image.filter(ImageFilter.CONTOUR)
    image = image.convert("L")
    image = ImageOps.posterize(image, 3)
    image = ImageOps.invert(image)
    image = ImageOps.colorize(
        image,
        black="black",
        mid="red",
        white="green")
    image = ImageChops.offset(
        image,
        xoffset=image.size[0] // 30,
        yoffset=image.size[1] // 30
    )

    return image

# def filters(image):
#     image = PIL.ImageOps.posterize(image, 1)
#     # image = PIL.ImageOps.solarize(image)
#     image = image.filter(ImageFilter.CONTOUR)
#     image = image.filter(ImageFilter.SHARPEN)
#     image = PIL.ImageOps.invert(image)
#     return image

def jpg_flow(path):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return

    image = resize(image)
    image = filters(image)

    image.save(path)

    return path
