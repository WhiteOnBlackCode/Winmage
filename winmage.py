"""
[*] Description:
    A tool to collect images from Windows Spotlight feature;
    This done by 
"""
import os
import shutil
import pathlib

from PIL import Image


def matchResolution(img_path):
    im = Image.open(img_path)
    return im.size == (1920, 1080)


class WinMage:
    IMG_DIR = pathlib.WindowsPath('.\\img')

    def __init__(self):
        if not self.IMG_DIR.exists():
            self.IMG_DIR.mkdir()
        
        self.locateAssetsDir()
        c_new = self.collectImages()
        print('[+] Added %d images' % c_new)

    def locateAssetsDir(self):
        self.assets_dir = pathlib.WindowsPath(
            f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets')
        if not self.assets_dir.exists():
            print('[X] No Spotlight directory found!')
            exit(2)

    def collectImages(self):
        c = 0
        for fn in os.listdir(self.assets_dir):
            asset_path = self.assets_dir / fn
            target_path = self.IMG_DIR / (fn + '.jpg')

            if target_path.exists():
                continue

            if matchResolution(asset_path):
                shutil.copy2(asset_path, target_path)
                c += 1
        return c


if __name__ == '__main__':
    WinMage()
