from __future__ import print_function
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='DepoBoxTool',
    version='2.0',
    author='Qian Shu',
    author_email='shumarkq@gmail.com',
    maintainer='Qian Shu',
    maintainer_email='shumarkq@gmail.com',
    url='https://github.com/shumarkq/DepoBoxTool',
    packages=['DepoBoxTool'],
    package_dir={'DepoBoxTool': 'src/DepoBoxTool'},
    install_requires = ['numpy', 'scipy', 'pandas']
)