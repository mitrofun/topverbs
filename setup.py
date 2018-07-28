import sys

from setuptools import setup, find_packages
from os.path import join, dirname

print(sys.path)

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of topverbs requires Python {}.{}
""")

setup(
    name='topverbs',
    scripts=['topverbs.py'],
    entry_points={'console_scripts': [
        'topverbs = topverbs:main',
    ]},
    version='1.1',
    install_requires=['nltk>=3'],
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    url='https://github.com/mitrofun/topverbs',
    description='The funniest joke in the world',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Analytics',
    ],
    keywords='verbs function name',
    author='Dmitry Shesterkin',
    author_email='mitri4@bk.ru',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    zip_safe=False
)
