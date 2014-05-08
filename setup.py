# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='natto',
    author='Thomas Schüßler',
    author_email='vindolin@gmail.com',
    url='github.com/vindolin/ninepatch',
    description='Slice and scale 9-patch images',
    long_description=open('README').read(),
    version='0.0.1',
    packages=['ninepatch'],
    license='MIT License',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.5',
                 'Topic :: Internet :: WWW/HTTP',
                 'Topic :: Software Development :: Debuggers',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 ],
)
