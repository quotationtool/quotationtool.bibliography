import zope.interface
import zope.component
import zope.schema
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.publisher.interfaces.browser import IBrowserRequest
from z3c.form.form import Form as ViewletForm
from z3c.form import field, button
from zope.viewlet.interfaces import IViewlet
from zope.app.component.hooks import getSite
from zope.traversing.api import traverse
from z3c.pagelet.browser import BrowserPagelet
from z3c.searcher.interfaces import ISearchSession

from quotationtool.search.interfaces import ISearchFilterProvider
from quotationtool.search.interfaces import ISearchResultPage

from quotationtool.bibliography.interfaces import _, IBibliography
from quotationtool.bibliography.searcher import BibliographySearchFilter


class BibliographySearchFilterProvider(object):
    """ Provide search for with search filter and information about it."""
    
    zope.interface.implements(ISearchFilterProvider)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    filterFactory = BibliographySearchFilter

    label = _('bibliographysearchfilterprovider-label', u"Bibliographic Entries")

    type_query = u'quotationtool.bibliography.interfaces.IEntry'

    session_name = 'bibliography'

    @property
    def resultURL(self):
        bibliography = zope.component.getUtility(
            IBibliography,
            context=self.context)
        return absoluteURL(bibliography, self.request) + u"/@@searchResult.html"


class SearchResultPage(BrowserPagelet):
    """ Found items."""
    
    zope.interface.implements(ISearchResultPage)

    session_name = 'bibliography'

    def getEntries(self):
        session = ISearchSession(self.request)
        fltr = session.getFilter(self.session_name)
        query = fltr.generateQuery()
        for obj in query.searchResults():
            yield obj
