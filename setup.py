from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='topverbs',
    entry_points={'console_scripts': [
        'topverbs = topverbs.topverbs:main',
    ]},
    version='1.1.1',
    install_requires=['nltk>=3'],
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    url='https://github.com/mitrofun/topverbs',
    description='Calculate the number of verbs used in function names in code.',
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
    tests_require=['pytest', 'pytest-flake8', 'flake8', 'mock'],
    test_suite='tests',
    zip_safe=False
)
