from distutils.core import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys
import os.path

PACKAGE = "flask_nav_bar"
NAME = "Flask-NavBar"
DESCRIPTION = "a navigator bar widgets"
AUTHOR = __import__(PACKAGE).__author__
AUTHOR_EMAIL = __import__(PACKAGE).__author_email__
URL = ""
VERSION = __import__(PACKAGE).__version__
DOC = __import__(PACKAGE).__doc__

setup(
    name=NAME,
    version=VERSION,
    long_description=__doc__,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    py_modules=["flask_nav_bar"],
    include_package_data=True,
    zip_safe=False,
    install_requires=open("requirements.txt").readlines(),
)

