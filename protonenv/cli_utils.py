import os
import argparse
import sys

# ---

# Reference: https://gist.github.com/mivade/384c2c41c3a29c637cb6c603d4197f9f

cli = argparse.ArgumentParser(description='Simple Proton version and prefix management.')
subparsers = cli.add_subparsers(dest="subcommand")

class Argument:
	def __init__(self, *name_or_flags, **kwargs):
		self.name_or_flags = list(name_or_flags)
		self.kwargs = kwargs

class MutuallyExclusiveGroup(Argument):
	def __init__(self, arguments, *name_or_flags, **kwargs):
		super().__init__(*name_or_flags, **kwargs)
		self.arguments = arguments

def subcommand(args=[], parent=subparsers, name=None):
    def decorator(func):
        parser = parent.add_parser(name or func.__name__, description=func.__doc__)
        for arg in args:
        	if isinstance(arg, MutuallyExclusiveGroup):
        		group = parser.add_mutually_exclusive_group(*arg.name_or_flags, **arg.kwargs)
        		for _arg in arg.arguments:
        			group.add_argument(*_arg.name_or_flags, **_arg.kwargs)
        	else:
        		parser.add_argument(*arg.name_or_flags, **arg.kwargs)
        parser.set_defaults(func=func)
    return decorator