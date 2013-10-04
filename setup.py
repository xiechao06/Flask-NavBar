from distutils.core import setup
from setuptools import find_packages

PACKAGE = "flask_nav_bar"
NAME = "flask-navbar"
DESCRIPTION = "a navigation bar widget for flask"
AUTHOR = 'xiechao'
AUTHOR_EMAIL = 'xiechao06@gmail.com'
URL = ""
VERSION = '0.9.0'
DOC = ''

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
    install_requires=open('requirements.txt').readlines(),
)

