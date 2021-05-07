import os
from dataclasses import dataclass

from .utils import json_load

# ---

HOME_DIR = os.path.expanduser("~")
PROTONENV_DIR = os.path.join(HOME_DIR, '.protonenv')


@dataclass
class Configuration:
	common_dir: str = os.path.join(HOME_DIR, '.steam/debian-installation/steamapps/common')
	protonenv_dir: str = PROTONENV_DIR
	prefixes_dir: str = os.path.join(PROTONENV_DIR, 'prefixes')
	temporary_dir: str = os.path.join(PROTONENV_DIR, 'temp')
	config_path: str = os.path.join(PROTONENV_DIR, 'config.json')

	def read_json(self):
		json_config = json_load(self.config_path)
		for k in ["common_dir", "protonenv_dir", "prefixes_dir", "temporary_dir", "config_path"]:
			if k in json_config:
				self.__setattr__(k, json_config[k])

		return self
# ---


config = Configuration().read_json()
