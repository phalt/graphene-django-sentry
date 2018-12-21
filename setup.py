#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'graphene_django==2.2.0',
    'sentry-sdk==0.5.2',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Paul Hallett",
    author_email='paulandrewhallett@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Capture Sentry exceptions in Graphene views",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='GraphQL graphene django sentry',
    name='graphene-django-sentry',
    packages=find_packages(include=['graphene_django_sentry']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/phalt/graphene-django-sentry',
    version='0.2.0',
    zip_safe=False,
)
