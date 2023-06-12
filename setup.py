from setuptools import setup, find_packages
import sys

from pydartpub import PYDARTPUB_VERSION

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 11)

if CURRENT_PYTHON < MIN_PYTHON:
    sys.stderr.writelines("This package required Python 3.11 or later")
    sys.exit(1)

setup(
    name = "pydartpub",
    version = PYDARTPUB_VERSION,
    author = "rk0cc",
    author_email = "enquiry@rk0cc.xyz",
    description = "Dart pub packages repository API client in Python",
    license = "BSD-3-Clause",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Dart",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP"
    ],
    keywords = [
        "Dart",
        "Flutter",
        "pub",
        "REST",
        "API"
    ],
    install_requires = [
        "versions>=1.6",
        "furl>=2"
    ],
    packages = find_packages(),
    python_requires = ">={0}.{1}, <4".format(*MIN_PYTHON)
)

