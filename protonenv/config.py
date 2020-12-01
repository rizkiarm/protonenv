import os

# ---

class Configuration(object):
	def __init__(self, dictionary=None):
		if dictionary is not None:
			self.__dict__.update(dictionary)

# ---

HOME_DIR = os.path.expanduser("~")

config = Configuration()
config.common_dir = os.path.join(HOME_DIR, '.steam/debian-installation/steamapps/common')
config.protonenv_dir = os.path.join(HOME_DIR, '.protonenv')
config.prefixes_dir = os.path.join(config.protonenv_dir, 'prefixes')
config.temporary_dir = os.path.join(config.protonenv_dir, 'temp')
config.config_path = os.path.join(config.protonenv_dir, 'config.json')