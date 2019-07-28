"""
[*] Description:
    A tool to collect images from Windows Spotlight feature;
    This done by 
"""
import os
import pathlib
import shutil

from src import *


class WinMage:
    def __init__(self):
        self.conf = Config()['DEFAULT']

        self.assets_dir = pathlib.WindowsPath(
            f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets')
        if not self.assets_dir.exists():
            print('[X] No Spotlight directory found!')
            exit(2)

        c_new = self.collectImages()
        print('[+] Added %d images' % c_new)

    def collectImages(self):
        c = 0
        for fn in os.listdir(str(self.assets_dir)):
            asset_path = self.assets_dir / fn
            target_path = pathlib.WindowsPath(self.conf['img_dir']) / (fn + '.jpg')

            if target_path.exists():
                continue

            if matchResolution(asset_path):
                shutil.copy2(asset_path, target_path)
                c += 1
        return c


if __name__ == '__main__':
    WinMage()
