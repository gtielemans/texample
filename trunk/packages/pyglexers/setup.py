"""
A small collection of lexers for use with Pygments.

The package adds support for:

- Sketch
- Dot (very basic)

"""
from setuptools import setup

__author__ = 'Kjell Magne Fauske'

setup(
    name='My pygment lexers',
    version='1.0',
    description=__doc__,
    author=__author__,
    packages=['pyglexers'],
    entry_points='''
    [pygments.lexers]
    mysketchlexer = pyglexers:SketchLexer
    mydotlexer = pyglexers:DotLexer
    '''
)