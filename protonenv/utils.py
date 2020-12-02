import json
import subprocess
import os
import re

# ---

# Source: https://stackoverflow.com/a/4836734

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)

# ---

def json_load(path):
	with open(path, 'r') as f:
		return json.load(f)

def json_dump(path, content):
	with open(path, 'w') as f:
		return json.dump(content, f)

# ---

def cmd_exec(command, env=None):
    if env is None:
    	env = {}
    env = {**env, **dict(os.environ)}
    subprocess.run(command, shell=True, env=env)

def exec_and_exit(*args, **kwargs):
	cmd_exec(*args, **kwargs)
	exit()

# ---

# Source: https://gist.github.com/garrettdreyfus/8153571#gistcomment-3519679

def yesno(question):
    prompt = f'{question} ? (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return yesno(question)
    if ans == 'y':
        return True
    return False

# ---

def die(message):
	print(message)
	exit()