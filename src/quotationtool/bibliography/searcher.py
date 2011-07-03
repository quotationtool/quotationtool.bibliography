import zope.interface
import zope.component
from z3c.searcher.interfaces import ISearchFilter, CONNECTOR_OR
from z3c.searcher.criterium import TextCriterium, SearchCriterium
from z3c.searcher.criterium import factory
from z3c.searcher.filter import EmptyTerm, SearchFilter
from zope.traversing.browser import absoluteURL

from quotationtool.search.interfaces import IQuotationtoolSearchFilter
from quotationtool.search.interfaces import ITypeExtent, ICriteriaChainSpecifier, IResultSpecifier
from quotationtool.search.interfaces import ICriteriumDescription

from quotationtool.bibliography.interfaces import _, IBibliography, IBibliographySearchFilter


class BibliographySearchFilter(SearchFilter):
    """ Bibliography search filter."""

    zope.interface.implements(IQuotationtoolSearchFilter,
                              IBibliographySearchFilter,
                              ITypeExtent,
                              ICriteriaChainSpecifier,
                              IResultSpecifier)

    def getDefaultQuery(self):
        return EmptyTerm()

    def delimit(self):
        """ See ITypeExtent"""
        crit = self.createCriterium('type-field')
        crit.value = u'quotationtool.bibliography.interfaces.IEntry'
        crit.connectorName = 'AND'
        self.addCriterium(crit)

    first_criterium_connector_name = CONNECTOR_OR # see ICriteriaChainSpecifier

    ignore_empty_criteria = True # see ICriteriaChainSpecifier

    def resultURL(self, context, request):
        """ See IResultSpecifier"""
        bibliography = zope.component.getUtility(
            IBibliography, context=context)
        return absoluteURL(bibliography, request) + u"/@@searchResult.html"

    session_name = 'bibliography' # see IResultSpecifier


bibliography_search_filter_factory = zope.component.factory.Factory(
    BibliographySearchFilter,
    _('BibliographyFilter-title', u"Bibliographic entries"),
    _('BibliographySearchFilter-desc', u"Search for entries in the bibliography.")
    )


class AuthorCriterium(TextCriterium):
    """ Full text criterium for 'author-fulltext' index."""

    zope.interface.implements(ICriteriumDescription)

    indexOrName = 'author-fulltext'

    label = _('author-fulltext-label', u"Author")

    description = _('author-fulltext-desc', u"Matches author or editor.")

    ui_weight = 110
    

author_factory = factory(AuthorCriterium, 'author-fulltext')


class TitleCriterium(TextCriterium):
    """ Full text criterium for 'title-fulltext' index."""

    zope.interface.implements(ICriteriumDescription)

    indexOrName = 'title-fulltext'

    label = _('title-fulltext-label', u"Title")

    description = _('title-fulltext-desc', u"Matches title, original title, subtitle and the like.")

    ui_weight = 120

title_factory = factory(TitleCriterium, 'title-fulltext')


