"""
[*] Description:
    A tool to collect images from Windows Spotlight feature;
    This done by...
"""
import os
import pathlib
import shutil
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


def locate_assets_dir():
    assets_dir = pathlib.Path.home() / 'AppData\\Local\\Packages'
    for i in os.listdir(assets_dir):
        if i.startswith('Microsoft.Windows.ContentDeliveryManager'):
            return assets_dir / i / 'LocalState\\Assets'

class WinMage:
    assets_dir = locate_assets_dir()

    def __init__(self):
        self.args = parse_args()
        self.config = Config()

        if not self.args.force and not self.config.should_run():
            log.warning('Already ran today!')
            exit(1)

        if not self.assets_dir.exists():
            log.error('No Spotlight directory found!')
            exit(2)

        self.perform()
        self.config.save()

    def perform(self):
        c_new = self.collect_images()
        if not c_new:
            log.info('Nothing added this time')
            return

        log.info(f'Added {len(c_new)} new images:')
        for i in c_new:
            log.info(f'New img #{c_new.index(i) + 1}: {i}')
        toaster = ToastNotifier()
        toaster.show_toast("Winmage", f"Added {len(c_new)} images!")

    def collect_images(self):
        c = []
        for fn in os.listdir(str(self.assets_dir)):
            asset_path = self.assets_dir / fn
            target_path = pathlib.WindowsPath(
                self.config['img_dir']) / (fn + '.jpg')

            if target_path.exists():
                continue

            if matchResolution(asset_path, self.config['scr_width'], self.config['scr_height']):
                shutil.copy2(asset_path, target_path)
                c.append(fn)
        return c


if __name__ == '__main__':
    WinMage()
