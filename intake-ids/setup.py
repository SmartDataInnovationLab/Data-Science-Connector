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
    install_requires=['intake', 'pandas', 'requests', 'pydantic', 'isodate'],
    long_description="",
    entry_points={
        'intake.drivers': [
            'connector_csv = intake_ids:ConnectorCSVSource',
            'connector = intake_ids.catalog:ConnectorCatalog'
        ]
    },
    zip_safe=False,
)