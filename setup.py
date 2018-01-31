from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ovt",
    version="0.2.1-dev",
    license='MIT',

    description="Ortho4XP Tile Validator",
    long_description=long_description,
    url="https://github.com/dyoung522/ovt",

    author="Donovan C. Young",
    author_email="dyoung522@gmail.com",

    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Utilities",
    ],
    keywords=["ortho4xp", "x-plane"],

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['colorama'],
    entry_points={'console_scripts': ['ovt=ovt:main']},
)

