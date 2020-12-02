# protonenv
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT) [![Python](https://img.shields.io/badge/python-3.6-blue)](https://www.python.org/downloads/release/python-360/) [![Steam Proton](https://img.shields.io/badge/steam-proton-brightgreen?logo=steam)](https://github.com/ValveSoftware/Proton)

Simple Proton version and prefix management.

A simple tool to manage different Proton versions and prefixes through the command line. The interface is designed to be similar to virtualenv management tools for ease-of-use. This tool is geared for those who want to run Windows programs easily without bloating their system with Wine and its dependencies. Although Proton is usable from the Steam client, it's not convenient to use for most scenarios, especially when installations are required. 

## Requirements

* Python >= 3.6
* Steam

## Installation
### PyPI (recommended)
```
pip install protonenv
```
### GitHub
#### Non-editable
```
pip install --upgrade git+https://github.com/rizkiarm/protonenv.git
```
You can upgrade the package by re-running the above command.
#### Editable
This option is recommended for development.

In the folder of your choosing, run the following command:
```
git clone https://github.com/rizkiarm/protonenv.git
cd protonenv/
pip install -e .
```
You can upgrade the package by running ``git pull`` from the ``protonenv`` folder.

## Usage
### Basic commands
```
protonenv versions
protonenv install {<version>,--list}
protonenv uninstall {<version>,<prefix>}
protonenv prefix <version> <prefix>
protonenv run <prefix> [command]
```
### Managing a prefix
```
protonenv default <prefix> --command <command> --flags <KEY1=VALUE1> [KEY2=VALUE2] ...
protonenv info <prefix>
protonenv directory <prefix> [--open]
```
The available flags (runtime config options) can be obtained from:
https://github.com/ValveSoftware/Proton#runtime-config-options
### More info
```
protonenv -h
protonenv -h {versions,install,uninstall,prefix,default,info,directory,run}
```

## Examples
### Basic example
Install Proton 5.0
```
protonenv install 5.0 
```
An example of installing and running [INSIDE](https://en.wikipedia.org/wiki/Inside_(video_game)):
```
# Create a new prefix called "inside"
protonenv prefix 5.0 inside 
# Run INSIDE's installer "Setup.exe" with prefix "inside"
protonenv run inside /path/to/INSIDE/Setup.exe
# Get the directory of drive C for prefix "inside"
DRIVE_C_DIR=$(protonenv directory inside | tail -1)
# Run INSIDE
PROTON_USE_WINED3D=1 protonenv run inside $DRIVE_C_DIR/path/to/INSIDE.exe
```
You can also set the flags and command as default for prefix "inside":
```
# Configure the default command and use wined3d environment variable by default
protonenv default inside --command $DRIVE_C_DIR/path/to/INSIDE.exe
protonenv default inside --flags PROTON_USE_WINED3D=1 
# Run INSIDE
protonenv run inside
```
### Directly running a program
An example of running ``program.exe`` with Proton 5.0
```
protonenv run 5.0 /path/to/program.exe
```
This command will execute the program in a temporary prefix with the specified Proton version. This is ideal for a situation where you want to test a program or you simply don't want to retain the program configuration/files.
## Uninstallation
```
pip uninstall protonenv
rm -rf ~/.protonenv
```