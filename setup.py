from distutils.core import setup

__author__ = "xiechao"
__author_email__ = "xiechao06@gmail.com"
__version__ = "0.9.0"

PACKAGE = "flask_nav_bar"
NAME = "Flask-NavBar"
DESCRIPTION = "a navigator bar widgets"
URL = ""

setup(
    name=NAME,
    version=__version__,
    long_description=__doc__,
    description=DESCRIPTION,
    author=__author__,
    author_email=__author_email__,
    license="MIT",
    py_modules=["flask_nav_bar"],
    include_package_data=True,
    zip_safe=False,
    install_requires=open("requirements.txt").readlines(),
)

