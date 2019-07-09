from os import mkdir, listdir, path, remove, rename
import shutil

from PIL import Image


def get_res(img_path):
    im = Image.open(img_path)
    return im.size


def main():
    assets = 'C:\\Users\\Handler\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'

    new = 'temp'
    c = 0

    try:
        mkdir(new)
    except FileExistsError:
        pass

    for fn in listdir(assets):
        src = path.join(assets, fn)
        dst = path.join(new, fn + '.jpg')
        shutil.copy2(src, dst)
    for n in listdir(new):
        fn = path.join(new, n)
        w, h = get_res(fn)
        if w != 1920 and h != 1080:
            remove(fn)
        else:
            try:
                rename(fn, path.join('img', n))
                c += 1
            except FileExistsError:
                pass
    print('Added %d images' % c)

    try:
        shutil.rmtree(new)
    except:
        print('ERROR Couldnt remove temp directory!')


if __name__ == '__main__':
    main()
