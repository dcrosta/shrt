from distribute_setup import use_setuptools
use_setuptools('0.6.c11')

from setuptools import setup, find_packages

setup(name='shrt',
      version='0.2',
      packages=['shrt'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[l for l in open('requirements.txt', 'r')],
)

