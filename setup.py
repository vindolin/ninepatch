# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ninepatch',
    version='0.1.0',
    author='Thomas Schüßler',
    author_email='vindolin@gmail.com',
    packages=['ninepatch', 'ninepatch.test'],
    scripts=['bin/ninepatch'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='MIT License',
    description='Slice and scale 9-patch images',
    long_description=open('README.txt').read(),
    install_requires=["pillow"],
)
