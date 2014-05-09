# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ninepatch',
    version='0.1.3',
    author='Thomas Schüßler',
    author_email='vindolin@gmail.com',
    packages=['ninepatch', 'ninepatch.test'],
    scripts=['bin/ninepatch'],
    url='https://github.com/vindolin/ninepatch',
    license=open('LICENSE').read(),
    description='Slice and scale 9-patch images',
    long_description=open('README.rst').read(),
    install_requires=["pillow"],
)
