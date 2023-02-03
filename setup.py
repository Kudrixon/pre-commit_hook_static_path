from setuptools import setup, find_packages

setup(
    name='check-static-path',
    version='1.0.2',
    packages=find_packages(include=['check-static-path', 'check-static-path.*'])
)