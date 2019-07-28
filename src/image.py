from PIL import Image


def matchResolution(img_path):
    im = Image.open(img_path)
    return im.size == (1920, 1080)
