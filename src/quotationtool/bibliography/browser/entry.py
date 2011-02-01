from zope.publisher.browser import BrowserView


class DefaultView(BrowserView):
    
    def __call__(self):
        return u"NOT IMPLEMENTED - view 'bibliography' for %s" % unicode(self.context.__class__)
