import zope.interface
from z3c.pagelet.browser import BrowserPagelet
from z3c.searcher.interfaces import ISearchSession

from quotationtool.search.interfaces import ISearchResultPage


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
