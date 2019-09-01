from PIL import Image


def matchResolution(img_path, scr_w, scr_h):
    im = Image.open(img_path)
    return im.size == (scr_w, scr_h)
