from z3c.pagelet.browser import BrowserPagelet
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.i18nmessageid import MessageFactory

from quotationtool.bibliography import interfaces


_ = MessageFactory('quotationtool')


class LabelView(BrowserView):
    
    def __call__(self):
        return _('bibliography-labelview',
                 u"Bibliography")


class Container(BrowserPagelet):
    """ A view that shows the contents of the bibliography."""

    def getEntries(self):
        return self.context.values()
