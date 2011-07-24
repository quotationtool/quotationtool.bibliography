import zope.interface
import zope.component
from z3c.table import table, column
from z3c.table.interfaces import ITable, IColumn
from zope.contentprovider.interfaces import IContentProvider
from z3c.pagelet.browser import BrowserPagelet

from quotationtool.bibliography.interfaces import _


class IBibliographyTable(ITable):
    """ A table representing the bibliographic entries."""


class BibliographyTable(table.Table, BrowserPagelet):
    """ The bibliography printed like a table."""

    zope.interface.implements(IBibliographyTable)

    render = BrowserPagelet.render

    cssClasses = {
        'table': u'container-listing',
        'thead': u"head",
        }
    cssClassEven = u"even"
    cssClassOdd = u"odd"


class IdColumn(column.LinkColumn):
    """ The id (__name__ attribute) of the bibliography table."""

    header = _('bibliography-columnheader-id',
               u"ID")

    weight = 10


class ISortingColumn(IColumn):
    """ A column that provides sorting table rows."""


class AuthorColumn(column.Column):
    """ The author column of the bibliography table."""

    zope.interface.implements(ISortingColumn)

    header = _('bibliography-columnheader-author',
               u"Author")
    weight = 100
    
    def renderCell(self, item):
        return zope.component.getMultiAdapter(
            (item, self.request), name='author')()


class TitleColumn(column.Column):
    """ The title column of the bibliography table."""

    zope.interface.implements(ISortingColumn)

    header = _('bibliography-columnheader-title',
               u"Title")
    weight = 200
    
    def renderCell(self, item):
        return zope.component.getMultiAdapter(
            (item, self.request), name='title')()


class YearColumn(column.LinkColumn):
    """ The year column of the bibliography table."""

    zope.interface.implements(ISortingColumn)

    header = _('bibliography-columnheader-year',
               u"Year")
    weight = 300
    
    def renderCell(self, item):
        return zope.component.getMultiAdapter(
            (item, self.request), name='year')()


class FlagsColumn(column.Column):
    """ The flags column of the bibliography table."""

    header = _('bibliography-columnheader-flags',
               u"flags")
    weight = 9999
    
    def renderCell(self, item):
        flags = zope.component.getMultiAdapter(
            (item, self.request, self.table), 
            IContentProvider, name='flags')
        flags.update()
        return flags.render()


