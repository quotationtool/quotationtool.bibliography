import unittest
import doctest
import zope.component
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig

import quotationtool.bibliography


_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS


def setUpZCML(test):
    """
        >>> import quotationtool.bibliography
        >>> from zope.configuration.xmlconfig import XMLConfig
        >>> XMLConfig('configure.zcml', quotationtool.bibliography)()

    """
    setUp(test)
    XMLConfig('configure.zcml', quotationtool.bibliography)()
    

class SiteCreationTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(SiteCreationTests, self).setUp()
        setUpZCML(self)

    def tearDown(self):
        tearDown(self)

    def test_BibliographyCreation(self):
        from quotationtool.site.site import QuotationtoolSite
        from quotationtool.bibliography.interfaces import IBibliography
        from quotationtool.bibliography.bibliography import Bibliography
        from zope.site.folder import rootFolder
        root = rootFolder()
        root['quotationtool'] = site = QuotationtoolSite()
        self.assertTrue(isinstance(site['bibliography'], Bibliography)) 
        ut = zope.component.queryUtility(
            IBibliography, context = site, default = None)
        self.assertTrue(ut == site['bibliography'])

    def test_CatalogIndexCreation(self):
        from quotationtool.site.site import QuotationtoolSite
        from quotationtool.bibliography.interfaces import IBibliographyCatalog
        from zope.site.folder import rootFolder
        root = rootFolder()
        root['quotationtool'] = site = QuotationtoolSite()
        from zope.catalog.interfaces import ICatalog
        ut = zope.component.queryUtility(
            ICatalog, name = 'bibliography', 
            context = site, default = None)
        from zc.catalog.extentcatalog import Catalog
        self.assertTrue(isinstance(ut, Catalog))


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp, tearDown = tearDown),
            doctest.DocTestSuite('quotationtool.bibliography.bibliography',
                                 setUp = setUp, 
                                 tearDown = tearDown,
                                 optionflags = _flags,
                                 ),
            doctest.DocFileSuite('README.txt',
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags = _flags,
                                 ),
            unittest.makeSuite(SiteCreationTests),
            ))
