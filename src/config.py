import configparser
import pathlib

CONF_PATH = pathlib.WindowsPath('.') / 'config.ini'
DEF_IMG_DIR = pathlib.WindowsPath('.') / 'img'


class Config(configparser.ConfigParser):
    def __init__(self):
        super(Config, self).__init__()

        if CONF_PATH.is_file():
            self.read(CONF_PATH)
            assert 'img_dir' in self[self.default_section]
        else:
            self[self.default_section] = {'img_dir': DEF_IMG_DIR.resolve()}
            with CONF_PATH.open('w') as f:
                self.write(f)

        img_dir = pathlib.WindowsPath(self[self.default_section]['img_dir'])
        if not img_dir.exists():
            img_dir.mkdir()
