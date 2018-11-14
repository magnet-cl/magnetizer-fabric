# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='magnetizer',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Fabric3>=1.14.post1',
        'Click>=7.0',
        'sh>=1.12.14',
    ],
    entry_points='''
    [console_scripts]
    magnetizer=magnetizer:cli
    ''',
    author='Joao López',
    author_email='joao@magnet.cl',
    url='http://magnetizer.magnet.cl/'
)
