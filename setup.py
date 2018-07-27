import topverbs
from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='topverbs',
    console_scripts={
        'console_scripts': [
            'topverbs = topverbs:main'
        ]
    },
    version=topverbs.__version__,
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
    author=topverbs.__author__,
    author_email='mitri4@bk.ru',
    license='MIT',
    zip_safe=False
)
