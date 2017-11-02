#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from setuptools import setup

setup(
	name = 'my_app',
	version = '1.0',
	license = 'GNU General Public Liscense v3',
	author = 'Pranjal',
	author_email = 'pranjalbhansali@yahoo.com',
	description = 'First Flask Setup',
	packages = ['my_app'],
	platforms = 'any',
	install_requires = ['flask',],
	classifiers = ['Development Status :: 4 - Beta',
					'Environment :: Web Environment',
					'Inteded Audience :: Developers',
					'Liscense:: OSI Approved :: GNU General Public Liscense v3',
					'Operating System :: OS Independent',
					'Programming Language :: Python',
					'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
					'Topic :: Software Development :: Libraries :: Python Module'
					],
	)