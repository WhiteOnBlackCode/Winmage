import json
import pathlib
from datetime import date, timedelta
import logging

log = logging.getLogger('root')

CONF_PATH = pathlib.WindowsPath('.') / 'config.json'
DEF_IMG_DIR = pathlib.WindowsPath('.') / 'img'

DEFAULT_CONF = {'img_dir': str(DEF_IMG_DIR.resolve()), 'last_day': date.today().isoformat(),
                'scr_width': 1920, 'scr_height': 1080}


class Config(dict):
    def __init__(self):
        super(Config, self).__init__()
        self.generated = False

        # Loading
        if CONF_PATH.is_file():
            try:
                with CONF_PATH.open() as f:
                    self.update(json.load(f))
                # Check existance of config keys
                if [x for x in DEFAULT_CONF if x not in self]:
                    self.generate()
            except json.JSONDecodeError:
                self.generate()
        else:
            self.generate()

        # Self now should be prepared by now
        img_dir = pathlib.WindowsPath(self['img_dir'])
        if not img_dir.exists():
            img_dir.mkdir()

    def generate(self):
        log.info('Generating config')
        self.clear()
        self.update(DEFAULT_CONF)
        self.save()
        self.generated = True

    def save(self):
        self['last_day'] = date.today().isoformat()

        # Write configuration into file
        with CONF_PATH.open('w') as f:
            json.dump(self, f, indent=4)

    def should_run(self) -> bool:
        if self.generated:
            return True
        last_day = date.fromisoformat(self['last_day'])
        return last_day + timedelta(days=1) <= date.today()
