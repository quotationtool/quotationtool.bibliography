from zope.publisher.browser import BrowserView
from z3c.pagelet.browser import BrowserPagelet
from zope.viewlet.manager import ViewletManager, WeightOrderedViewletManager

from quotationtool.bibliography import interfaces


class DefaultView(BrowserView):
    
    def __call__(self):
        return u"NOT IMPLEMENTED - view 'bibliography' or 'citation' for %s" % unicode(self.context.__class__)


class AddEntry(BrowserPagelet):
    """A pagelet that lets the user add an entry to the bibliography."""


AddEntryManager = ViewletManager('add-bibliographic-entry',
                                 interfaces.IAddEntryManager,
                                 bases = (WeightOrderedViewletManager,))
                                 
    
