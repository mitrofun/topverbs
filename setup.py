import topverbs
from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='topverbs',
    version=topverbs.__version__,
    install_requires=['nltk>=3'],
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    url='https://github.com/mitrofun/topverbs',
)
