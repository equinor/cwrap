#!/usr/bin/env python

from setuptools import setup, Extension

long_description = """
=======
cwrap
=======

Introduction
------------

Cwrap is a meta library using ctypes to quickly load and call C functions from
Python. It's primarily desgined to be practicaul and useful for the ecl
library https://github.com/statoil/libecl, but isn't tied to it.
"""

setup(name='cwrap',
      use_scm_version={'write_to': 'cwrap/version.py' },
      description='cwrap - ctypes blanket',
      long_description=long_description,
      author='Statoil ASA',
      author_email='fg_gpl@statoil.com',
      url='https://github.com/Statoil/cwrap',
      packages=['cwrap'],
      setup_requires=['setuptools_scm'],
      license='GPL-3.0',
      platforms='any',
      install_requires=['six'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities'
      ],
      test_suite='tests',
)
