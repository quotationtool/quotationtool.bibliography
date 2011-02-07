import unittest
import doctest
import zope.component
import zope.publisher.interfaces
import zope.publisher.browser
import z3c.form
from zope.component.testing import setUp, tearDown, PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
from zope.security.testing import Principal

from quotationtool.skin.interfaces import IQuotationtoolBrowserLayer 

import quotationtool.bibliography
import quotationtool.bibliography.browser


_flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS

anonymous = Principal('anonymous')


def setUpZCML(test):
    setUp(test)
    # browser package is loaded 
    XMLConfig('configure.zcml', quotationtool.bibliography)()
    

class MyEntry(object):

    zope.interface.implements(quotationtool.bibliography.interfaces.IEntry)
    
    def __init__(self, author = u'', title = u'', year = -10000):
        self.author = author
        self.title = title
        self.year = year

    __name__ = __parent__ = None


def generateContent(test):
    from quotationtool.bibliography.bibliography import Bibliography
    biblio = Bibliography()
    biblio['KdU'] = MyEntry(u'Kant', u'KdU', 1790)
    from zope.location.interfaces import IRoot
    zope.interface.directlyProvides(biblio, IRoot)
    return biblio



class TestRequest(zope.publisher.browser.TestRequest):
    # we have to implement the layer interface which the templates and
    # layout are registered for. See the skin.txt file in the
    # zope.publisher.browser module.
    zope.interface.implements(
        z3c.form.interfaces.IFormLayer,
        IQuotationtoolBrowserLayer)


class ContainerTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(ContainerTests, self).setUp()
        setUpZCML(self)

    def OFFtest_ContainerPagelet(self):
        biblio = generateContent(self)
        request = TestRequest()
        view = zope.component.getMultiAdapter(
            (biblio, request),
            zope.publisher.interfaces.browser.IBrowserView,
            name = 'index.html',
            )
        self.assertTrue(isinstance(view(), unicoded))

    def test_ContainerPagelet(self):
        biblio = generateContent(self)
        request = TestRequest()
        request.setPrincipal(anonymous)
        from quotationtool.bibliography.browser.bibliography import Container
        view = Container(biblio, request)
        self.assertTrue(isinstance(view(), unicode))
        

class EntryTests(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(EntryTests, self).setUp()
        setUpZCML(self)

    def test_AddEntryPagelet(self):
        biblio = generateContent(self)
        request = TestRequest()
        request.setPrincipal(anonymous)
        from quotationtool.bibliography.browser.entry import AddEntry
        view = AddEntry(biblio, request)
        self.assertTrue(isinstance(view(), unicode))
        

def test_suite():
    return unittest.TestSuite((
            unittest.makeSuite(ContainerTests),
            unittest.makeSuite(EntryTests),
            ))
