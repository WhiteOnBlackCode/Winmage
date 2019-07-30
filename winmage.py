"""
[*] Description:
    A tool to collect images from Windows Spotlight feature;
    This done by 
"""
import os
import pathlib
import shutil
from datetime import date, timedelta

from src import *


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', default=False, action='store_true')
    return parser.parse_args()


class WinMage:
    def __init__(self):
        self.args = parse_args()
        self.config = Config()
        self.section = self.config[self.config.default_section]

        if not self.args.force and not self.config.should_run():
            exit('[!] Already ran today!')

        self.assets_dir = pathlib.WindowsPath(
            f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets')
        if not self.assets_dir.exists():
            print('[X] No Spotlight directory found!')
            exit(2)

        c_new = self.collect_images()
        print('[+] Added %d images' % c_new)
        self.config.save()

    def collect_images(self):
        c = 0
        for fn in os.listdir(str(self.assets_dir)):
            asset_path = self.assets_dir / fn
            target_path = pathlib.WindowsPath(
                self.section['img_dir']) / (fn + '.jpg')

            if target_path.exists():
                continue

            if matchResolution(asset_path):
                shutil.copy2(asset_path, target_path)
                c += 1
        return c


if __name__ == '__main__':
    WinMage()
