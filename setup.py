import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# ---

# SOURCE: https://github.com/navdeep-G/setup.py

# ---

# METADATA
NAME = 'protonenv'
DESCRIPTION = 'Simple Proton version and prefix management.'
URL = 'https://github.com/rizkiarm/protonenv'
EMAIL = 'rizki@rizkiarm.com'
AUTHOR = 'Muhammad Rizki Aulia Rahman Maulana'
REQUIRES_PYTHON = '>=3.6.0'
KEYWORDS = ['steam', 'proton', 'prefix', 'wine']

# ---

# README
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

# VERSION
about = {}
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(here, project_slug, '__version__.py')) as f:
    exec(f.read(), about)
VERSION = about['__version__']

# ---

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
        
        ans = input("Are you sure you want to publish?\n").strip().lower()
        if ans not in ['y']: exit()

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()

# ---

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author = AUTHOR,
    author_email = EMAIL,
    url = URL,
    keywords = KEYWORDS,
    license="MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages = find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "protonenv=protonenv:main",
        ],
    },
    python_requires=REQUIRES_PYTHON,
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)