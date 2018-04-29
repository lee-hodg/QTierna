# -*- coding: utf-8 -*-
"""Simple reminders app"""
from setuptools import setup

with open('README.md') as README:
    LONG_DESCRIPTION = README.read()

setup(
    name='qtierna',
    version='1.0.0',
    url='https://gitlab.com/fpghost/qtierna',
    license='MIT',
    author='Lee H',
    author_email='lee@logicon.io',
    description="Simple reminders app",
    keywords='PyQt Reminders',
    long_description=LONG_DESCRIPTION,
    install_requires=['arrow', 'PySide', 'python-dateutil', 'pytz', 'six', 'SQLAlchemy', 'tzlocal'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
    ],
    packages=['qtierna', ]
)
