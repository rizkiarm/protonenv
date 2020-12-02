import os
import shutil
import glob
import shlex

from .config import config
from .utils import *
from .core_utils import *
from .cli_utils import *

# ---

HOME_DIR = os.path.expanduser("~")
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
proton_appids = json_load(os.path.join(SCRIPT_DIR, 'proton.json'))

# ---

def proton_exec(version, prefix_name, command, flags=None):
	proton_exec_path = get_proton_exec_path(version)
	proton_exec_path = shlex.quote(proton_exec_path)
	command 		 = shlex.quote(command)
	if prefix_name is None:
		path = get_temporary_path()
		os.makedirs(path)
	else:
		path = get_prefix_path(prefix_name)
	env = {'STEAM_COMPAT_DATA_PATH': path}
	if flags is not None:
		for k,v in flags.items():
			env[k] = v
	cmd_exec(f'{proton_exec_path} waitforexitandrun {command}', env=env)

def ask_common_dir():
	while True:
		ans = input(f"Steam app common directory? (default: {config.common_dir}) [y to accept]\n").strip().lower()
		if ans == 'y':
			ans = config.common_dir
		if os.path.exists(ans):
			break
		print(f'{ans} does not exists, try again...')
	return ans


def setup():
	global config
	if not os.path.exists(config.protonenv_dir):
		print(f'Creating protonenv directory: {config.protonenv_dir}')
		os.makedirs(config.protonenv_dir)
	if not os.path.exists(config.prefixes_dir):
		print(f'Creating prefixes directory: {config.prefixes_dir}')
		os.makedirs(config.prefixes_dir)
	if not os.path.exists(config.temporary_dir):
		print(f'Creating temporary directory: {config.temporary_dir}')
		os.makedirs(config.temporary_dir)
	if not os.path.exists(config.config_path):
		config.common_dir = ask_common_dir()
		print(f'Creating config file: {config.config_path}')
		config_save(config)
	else:
		config = config_load()

def cleanup():
	for path in glob.glob(os.path.join(config.temporary_dir, '*')):
		assert HOME_DIR in path and '.protonenv' in path and config.protonenv_dir in path # be extra careful
		n_active = int(subprocess.check_output(f'lsof +d {path} | tail -n +2 | wc -l', shell=True))
		if n_active == 0:
			print(f'Cleaning up: {path}')
			shutil.rmtree(path)

def init():
	setup()
	cleanup()

# ---

@subcommand([])
def versions(args):
	for path in natural_sort(glob.glob(os.path.join(config.common_dir, 'Proton *'))):
		version = os.path.basename(path).split(' ')[-1]
		if not proton_exists(version):
			continue
		print(f'{version}')
	for path in natural_sort(glob.glob(os.path.join(config.prefixes_dir, '*'))):
		prefix_name = os.path.basename(path)
		prefix_config = prefix_config_load(prefix_name)
		print(f"{prefix_name} [{prefix_config['version']}]")

@subcommand([MutuallyExclusiveGroup([Argument("version", help="Proton version", nargs='?', default=None), 
									 Argument("--list", help="List installable Proton versions", action="store_true")], required=True)
			])
def install(args):
	if args.list:
		for version,_ in proton_appids.items():
			print(version, "\t[installed]" if proton_exists(version) else '')
		exit()
	if proton_exists(args.version):
		die(f'Proton {args.version} has already been installed.')
	appid = proton_appids.get(args.version)
	if appid is not None:
		exec_and_exit(f'steam steam://install/{appid}')
	die(f'Version {args.version} not found.')

@subcommand([Argument("name", help="Proton version or prefix name")])
def uninstall(args):
	appid = proton_appids.get(args.name)
	if appid is not None:
		exec_and_exit(f'steam steam://uninstall/{appid}')
	if not prefix_exists(args.name):
		die(f'Version {args.name} not found.')
	prefix_path = get_prefix_path(args.name)
	if yesno(f'Do you want to delete: {prefix_path}'):
		print(f'Deleting: {prefix_path}')
		shutil.rmtree(prefix_path)
	else:
		die('Nothing to do.')

@subcommand([Argument("version", help="Proton version"), Argument("prefix", help="Prefix name")])
def prefix(args):
	if prefix_exists(args.prefix):
		die(f'Prefix "{args.prefix}" has already exists.')
	if not proton_exists(args.version):
		die(f'Proton {args.version} does not exists.')
	os.makedirs(get_prefix_path(args.prefix))
	prefix_config = {"version": args.version}
	prefix_config_save(args.prefix, prefix_config)
	proton_exec(args.version, args.prefix, '') # initialize Proton prefix

@subcommand([Argument("prefix", help="Prefix name"), Argument("--flags", help="Environment variable: KEY=VALUE", nargs='+'), Argument("--command", help="Default command")])
def default(args):
	if not prefix_exists(args.prefix):
		die(f'Prefix {args.prefix} does not exists.')
	prefix_config = prefix_config_load(args.prefix)
	if args.command:
		prefix_config['command'] = args.command
		print(f'\"{prefix_config["command"]}\" will be run by default')
	if args.flags:
		prefix_config['flags'] = {}
		for flag in args.flags:
			try:
				k, v = flag.split('=')
			except:
				die('Invalid flag, it must be in the form of KEY=VALUE.')
			prefix_config['flags'][k] = v
		print(f'{prefix_config["flags"]} is set by default')
	if args.command or args.flags:
		prefix_config_save(args.prefix, prefix_config)
	else:
		die('Nothing to do.')

@subcommand([Argument("prefix", help="Prefix name")])
def info(args):
	if not prefix_exists(args.prefix):
		die(f'Prefix {args.prefix} does not exists.')
	prefix_config = prefix_config_load(args.prefix)
	die(f'\
{args.prefix}\n\
{"-"*len(args.prefix)}\n\
Proton\t: {prefix_config["version"]}\n\
Command\t: {prefix_config.get("command")}\n\
Flags\t: {prefix_config.get("flags")}\
		')

@subcommand([Argument("prefix", help="Prefix name"), Argument("--open", action="store_true", help="Open the directory")])
def directory(args):
	if not prefix_exists(args.prefix):
		die(f'Prefix {args.prefix} does not exists.')
	content_path = get_prefix_content_path(args.prefix)
	if args.open:
		cmd_exec(f'xdg-open {content_path}')
	die(content_path)

@subcommand([Argument("name", help="Proton version or prefix name"), Argument("command", nargs='?', default=None, help="Command to execute")])
def run(args):
	if not prefix_exists(args.name):
		if not proton_exists(args.name):
			die(f'{args.name} does not exists.')
		if not args.command:
			die('Command is not specified.')
		proton_exec(args.name, None, args.command)
		exit()
	prefix_config = prefix_config_load(args.name)
	command = args.command or prefix_config.get('command')
	if command is None:
		die("Command is not specified and the default command is also not set.")
	flags = prefix_config.get('flags')
	version = prefix_config.get('version')
	proton_exec(version, args.name, command, flags)

def main():
	init()
	args = cli.parse_args()
	if args.subcommand is None:
		cli.print_help()
	else:
		args.func(args)