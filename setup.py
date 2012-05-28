from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(name='shrt',
      version='0.2',
      packages=['shrt'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[l for l in open('requirements.txt', 'r')],
)

