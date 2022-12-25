#! /usr/bin/env python

import os
from setuptools import setup, find_packages

def get_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        return f.read()

setup(

    # プラグイン名 = パッケージの名前
    name='unicon.plugins.fitelnet',

    version='1.0',

    description='Unicon Plugin for FITELnet',

    long_description=get_readme(),

    url='https://github.com/takamitsu-iida',

    author='takamitsu-iida',

    author_email='',

    license='Apache 2.0',

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='pyats unicon plugin connection',

    packages=find_packages(where='src'),

    package_dir={
        '': 'src',
    },

    package_data={},

    # see https://developer.cisco.com/docs/unicon/
    # entry_points = {'unicon.plugins': ['<platform_name> = <module_name>']},
    entry_points={'unicon.plugins': ['fitelnet=unicon.plugins.fitelnet']},
    install_requires=['setuptools', 'unicon'],
    extras_require={},
    data_files=[],
    cmdclass={},
    zip_safe=False,
)
