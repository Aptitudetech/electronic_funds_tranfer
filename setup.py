# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

import re, ast

# get version from __version__ variable in electronic_funds_transfer/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('electronic_funds_transfer/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = parse_requirements("requirements.txt", session="")

setup(
	name='electronic_funds_transfer',
	version=version,
	description=' Electronic Funds Transfer (EFT) Direct Deposit is an electronic payment service that provides your business with a fast and simple way to issue Canadian and U.S. dollar payments to accounts at any financial institution in Canada.',
	author='CloudGround / Aptitudetech',
	author_email='support@cloudground.ca',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[str(ir.req) for ir in requirements],
	dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
