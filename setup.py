from setuptools import setup, find_packages

setup(name='protonenv',
    version='0.1',
    author="Muhammad Rizki Aulia Rahman Maulana",
    author_email="rizki@rizkiarm.com",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "protonenv=protonenv.core:main",
        ],
    },
)