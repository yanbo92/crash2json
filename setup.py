# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 10:26 下午
# @Author  : yanbo92
# @File    : setup.py

from distutils.core import setup
from setuptools import find_packages

setup(name='crash2json',
      version='2.7',
      description='Parse appple crash report to json file',
      author='yanbo92',
      author_email='yanbo92@139.com',
      url='https://github.com/yanbo92/crash2json',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'crash2json = crash2json.__main__:main',

          ]
      }
      )
