#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='intake-ids',
    version='0.0.1',
    description='IDS plugin',
    url='',
    maintainer='Omer Erdinc Yagmurlu',
    maintainer_email='',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['intake', 'pandas'],
    long_description="",
    entry_points={
        'intake.drivers': [
            'connector = intake_ids:ConnectorSource',
        ]
    },
    zip_safe=False,
)