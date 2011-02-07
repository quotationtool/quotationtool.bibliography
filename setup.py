# -*- coding: utf-8 -*-
"""Setup for quotationtool.bibliography package

$Id$
"""
from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name='quotationtool.bibliography'

setup(
    name = name,
    version='0.1.0',
    description="Bibliography folder the quotationtool application",
    long_description=(
        read('README')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'quotationtool', 'bibliography', 'README.txt')
        + '\n' +
        'Download\n'
        '********\n'
        ),
    keywords='quotationtool',
    author=u"Christian Lueck",
    author_email='cluecksbox@googlemail.com',
    url='',
    license='ZPL 2.1',
    # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python',
                 'Environment :: Web Environment',
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                 'Framework :: BlueBream',
                 ],
    packages = find_packages('src'),
    namespace_packages = ['quotationtool',],
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'setuptools',
        'ZODB3',
        'zope.interface',
        'zope.schema',
        'zope.component',
        'zope.container',
        'zope.exceptions',
        'zope.i18nmessageid',
        'zope.catalog',
        'zc.catalog >= 1.5',
        'zope.app.content',
        'zope.annotation',
        'zope.dublincore',
        'zope.security',
        'zope.securitypolicy',
        'zope.app.schema',
        'zope.viewlet',

        'quotationtool.site',
        'quotationtool.security',
        'quotationtool.skin',
        'quotationtool.search',

        'z3c.template',
        'z3c.macro',
        'z3c.pagelet',
        'z3c.layer.pagelet',
        'zope.app.publication',
        'zope.browserpage',
        'zope.publisher',
        'z3c.formui',
        'z3c.form',
        'zc.resourcelibrary',
        'z3c.menu.ready2go',

        'zope.app.pagetemplate',
        'zope.app.component',
        ],
    extras_require = dict(
        test = [
            'zope.testing',
            'zope.configuration',
            'zope.site',
            ],
        ),
    )
