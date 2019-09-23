"""
[*] Description:
    A tool to collect images from Windows Spotlight feature;
    This done by 
"""
import os
import pathlib
import shutil
from datetime import date, timedelta
import logging as log

from win10toast import ToastNotifier

from src import *

log.basicConfig(filename='log.txt', level=log.INFO,
                format='%(asctime)s::%(levelname)s::%(message)s', datefmt='%H:%M:%S')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', default=False, action='store_true')
    return parser.parse_args()


class WinMage:
    def __init__(self):
        self.args = parse_args()
        self.config = Config()

        if not self.args.force and not self.config.should_run():
            log.warning('Already ran today!')
            exit(1)

        self.assets_dir = pathlib.WindowsPath(
            f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets')
        if not self.assets_dir.exists():
            log.err('No Spotlight directory found!')
            exit(2)

        c_new = self.collect_images()
        if not c_new:
            log.info('Nothing added this time')
        else:
            log.info('Added %d images' % c_new)
            toaster = ToastNotifier()
            toaster.show_toast("Winmage", "Added %d images!" % c_new)
        self.config.save()

    def collect_images(self):
        c = 0
        for fn in os.listdir(str(self.assets_dir)):
            asset_path = self.assets_dir / fn
            target_path = pathlib.WindowsPath(
                self.config['img_dir']) / (fn + '.jpg')

            if target_path.exists():
                continue

            if matchResolution(asset_path, self.config['scr_width'], self.config['scr_height']):
                shutil.copy2(asset_path, target_path)
                c += 1
        return c


if __name__ == '__main__':
    WinMage()
