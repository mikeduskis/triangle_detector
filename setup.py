import os
import sys
import unittest

from setuptools import Command, setup, find_packages

MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = 0


def version_number():
    return '%d.%d.%d' % (MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)


class TestRunner(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        unittest.main(module=None, argv=[sys.argv[0], 'discover'])


setup(name='triangle_detector',
      version=version_number(),
      description='Web service that attempts to detect triangles',
      url='https://gitlab.int.protectwise.net/testing/triangle-detector',
      author='Mike Duskis',
      author_email='mike.duskis@protectwise.com',
      license='proprietary',
      packages=find_packages(),
      include_package_data=True,
      exclude_package_data={'': ['tests']},
      install_requires=[
          'expects',
          'flask>=0.12.2',
          'requests'],
      cmdclass={'test': TestRunner}
      )
