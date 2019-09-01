import json
import pathlib
from datetime import date, timedelta

CONF_PATH = pathlib.WindowsPath('.') / 'config.json'
DEF_IMG_DIR = pathlib.WindowsPath('.') / 'img'

DEF_CONF = {'img_dir': str(DEF_IMG_DIR.resolve()), 'last_day': date.today().isoformat(),
            'scr_width': 1920, 'scr_height': 1080}


class Config(dict):
    def __init__(self):
        super(Config, self).__init__()

        # Loading
        if CONF_PATH.is_file():
            try:
                with CONF_PATH.open() as f:
                    json.load(f)
                if [x for x in DEF_CONF if x not in self]:
                    self.generate()
            except json.JSONDecodeError:
                self.generate()
        else:
            self.generate()

        img_dir = pathlib.WindowsPath(self['img_dir'])
        if not img_dir.exists():
            img_dir.mkdir()

    def generate(self):
        self.clear()
        self.update(DEF_CONF)
        self.save()

    def save(self):
        self['last_day'] = date.today().isoformat()

        with CONF_PATH.open('w') as f:
            json.dump(self, f, indent=4)

    def should_run(self) -> bool:
        last_day = date.fromisoformat(self['last_day'])
        return last_day + timedelta(days=1) <= date.today()
