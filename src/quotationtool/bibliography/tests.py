import unittest
import doctest
import zope.component
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
from zope.app.testing.setup import placefulSetUp, placefulTearDown
from zope.site.folder import rootFolder

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
    
def setUpSome(test):
    """ There are subscribers that need intid in the dependencies
    (zope.catalog)"""
    import zope
    # some dependencies
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('meta.zcml', zope.security)()
    XMLConfig('meta.zcml', zope.securitypolicy)()
    
    XMLConfig('configure.zcml', zope.component)()
    XMLConfig('configure.zcml', zope.security)()
    XMLConfig('configure.zcml', zope.site)()
    XMLConfig('configure.zcml', zope.annotation)()
    XMLConfig('configure.zcml', zope.dublincore)()
    XMLConfig('configure.zcml', quotationtool.site)()
    # subscribers
    from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
    zope.component.provideHandler(
        quotationtool.bibliography.bibliography.createBibliography,
        adapts=[INewQuotationtoolSiteEvent])
    zope.component.provideHandler(
        quotationtool.bibliography.indexing.createBibliographyCatalog,
        adapts=[INewQuotationtoolSiteEvent])
    # bibliography object annotation
    from zope.annotation.interfaces import IAttributeAnnotatable
    from quotationtool.bibliography.bibliography import Bibliography
    zope.interface.classImplements(Bibliography, IAttributeAnnotatable)


class SiteCreationTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(SiteCreationTests, self).setUp()
        setUpSome(self)
        self.root_folder = rootFolder()

    def tearDown(self):
        placefulTearDown()
        tearDown(self)

    def test_BibliographyCreation(self):
        from quotationtool.site.site import QuotationtoolSite
        from quotationtool.bibliography.interfaces import IBibliography
        from quotationtool.bibliography.bibliography import Bibliography
        self.root_folder['quotationtool'] = site = QuotationtoolSite()

        self.assertTrue(isinstance(site['bibliography'], Bibliography)) 
        ut = zope.component.queryUtility(
            IBibliography, context = site, default = None)
        self.assertTrue(ut == site['bibliography'])

    def test_CatalogIndexCreation(self):
        from quotationtool.site.site import QuotationtoolSite
        from quotationtool.bibliography.interfaces import IBibliographyCatalog
        self.root_folder['quotationtool'] = site = QuotationtoolSite()
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
