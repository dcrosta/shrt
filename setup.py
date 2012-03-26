from setuptools import setup, find_packages

requires = [
    'flask',
    'pymongo',
]

setup(name='shrt',
      version='0.1',
      packages=['shrt'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      entry_points={
          'paste.app_factory': ['main=shrt:app_factory'],
      }
)

