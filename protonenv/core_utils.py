import os
import time
from .config import config, Configuration
from .utils import json_load, json_dump

# ---

def get_proton_path(version):
	return os.path.join(config.common_dir, f'Proton {version}')

def get_proton_exec_path(version):
	return os.path.join(get_proton_path(version), 'proton')

def get_prefix_path(prefix_name):
	return os.path.join(config.prefixes_dir, prefix_name)

def get_prefix_content_path(prefix_name):
	return os.path.join(get_prefix_path(prefix_name), 'pfx/drive_c')

def get_temporary_path():
	return os.path.join(config.temporary_dir, str(time.time()))

def get_prefix_config_path(prefix_name):
	return os.path.join(get_prefix_path(prefix_name), 'config.json')

def prefix_exists(prefix_name):
	return os.path.exists(get_prefix_path(prefix_name))

def proton_exists(version):
	return os.path.exists(get_proton_exec_path(version))

def config_load():
	return Configuration(json_load(config.config_path))

def config_save(content):
	json_dump(config.config_path, vars(content))
	
def prefix_config_load(prefix_name):
	return json_load(get_prefix_config_path(prefix_name))

def prefix_config_save(prefix_name, content):
	json_dump(get_prefix_config_path(prefix_name), content)