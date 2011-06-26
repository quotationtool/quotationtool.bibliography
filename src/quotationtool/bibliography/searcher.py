import zope.interface
from z3c.searcher.interfaces import ISearchFilter
from z3c.searcher.criterium import TextCriterium, SearchCriterium
from z3c.searcher.criterium import factory
from z3c.searcher.filter import EmptyTerm, SearchFilter

from quotationtool.search.interfaces import ITypeExtent

from quotationtool.bibliography.interfaces import _


class IBibliographySearchFilter(ISearchFilter):
    """ Search filter for bibliographic entries."""


class BibliographySearchFilter(SearchFilter):
    """ Bibliography search filter."""

    zope.interface.implements(IBibliographySearchFilter,
                              ITypeExtent)

    def getDefaultQuery(self):
        return EmptyTerm()

    def delimit(self):
        """ See ITypeExtent"""
        crit = self.createCriterium('type-field')
        crit.value = u'quotationtool.bibliography.interfaces.IEntry'
        crit.connectorName = 'AND'
        self.addCriterium(crit)


class AuthorCriterium(TextCriterium):
    """ Full text criterium for 'author-fulltext' index."""

    indexOrName = 'author-fulltext'

    label = _('author-fulltext-label', u"Author")

author_factory = factory(AuthorCriterium, 'author-fulltext')


class TitleCriterium(TextCriterium):
    """ Full text criterium for 'title-fulltext' index."""

    indexOrName = 'title-fulltext'

    label = _('title-fulltext-label', u"Title")

title_factory = factory(TitleCriterium, 'title-fulltext')


