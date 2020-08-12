#!/usr/bin/env python
"""
Setup script
"""

from setuptools import setup

try:
    import logging
    import multiprocessing
except ImportError:
    pass


def strip_comments(lines):
    for line in lines:
        line = line.strip()

        if line.startswith('#'):
            continue

        if not line:
            continue

        if not '#' in line:
            yield line
        else:
            yield line[:line.index('#')]


def get_requires(filename="requirements.txt"):
    with open(filename, 'r') as f:
        return list(strip_comments(f.readlines()))

setup(
    name='datagrepper',
    description='A webapp to query fedmsg history',
    version='0.9.6',
    author='Ian Weller and Ralph Bean',
    author_email='ianweller@fedoraproject.org, ralph@fedoraproject.org',
    license='GPLv2+',
    url='https://github.com/fedora-infra/datagrepper/',
    packages=['datagrepper'],
    include_package_data=True,
    install_requires=get_requires(),
    tests_require=get_requires(filename='test-requirements.txt'),
    test_suite='nose.collector',
)
