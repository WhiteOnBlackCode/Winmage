import configparser
import pathlib
from datetime import date, timedelta

CONF_PATH = pathlib.WindowsPath('.') / 'config.ini'
DEF_IMG_DIR = pathlib.WindowsPath('.') / 'img'


class Config(configparser.ConfigParser):
    def __init__(self):
        super(Config, self).__init__()

        # Loading
        if CONF_PATH.is_file():
            self.read(CONF_PATH)
            if [x for x in ('img_dir', 'last_day') if x not in self[self.default_section]]:
                self.generate()
        else:
            self.generate()

        img_dir = pathlib.WindowsPath(self[self.default_section]['img_dir'])
        if not img_dir.exists():
            img_dir.mkdir()

    def generate(self):
        self[self.default_section] = {'img_dir': DEF_IMG_DIR.resolve(),
                                      'last_day': date.today().isoformat()}
        self.save()

    def save(self):
        self[self.default_section]['last_day'] = date.today().isoformat()

        with CONF_PATH.open('w') as f:
            self.write(f)

    def should_run(self) -> bool:
        last_day = date.fromisoformat(self[self.default_section]['last_day'])
        return last_day + timedelta(days=1) <= date.today()
