from codecs import open
from os import path
from otv.globals import VERSION
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="otv",
    version=VERSION,
    license="MIT",

    description="Ortho4XP Tile Validator",
    long_description=long_description,
    url="https://github.com/dyoung522/otv",

    author="Donovan C. Young",
    author_email="dyoung522@gmail.com",

    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Utilities",
    ],
    keywords=["ortho4xp", "x-plane"],

    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,

    install_requires=["colorama", "tqdm"],
    python_requires=">=3",

    entry_points={"console_scripts": ["otv=otv:main"]},
)
