	#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = '1.0'

__build__ = ''

setup(
    name='atmospheres',
    version=__version__ + __build__,
    description='Atmospheres of San Francisco neighborhood',
    author='CSC868-Group2',
	author_email='ksweta007@gmail.com',
	url='https://github.com/eshlefest/atmospheres',
	packages=find_packages(exclude=['*.tests']),
	setup_requires=[
	  		'nose>=1.0'
    ],
	install_requires=[
        'tweepy', 
        'nltk',
        'pymongo',
        'flask',
	],
    tests_require=[
        'mock>=1.0.1',
        'coverage',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'atmospheres-web-service = atmospheres.server.web_service:main'
        ]
    },
    package_data={
    'static': 'atmospheres/static/*'
    }
    

)

