import zope.component
from z3c.indexer.index import FieldIndex, TextIndex, ValueIndex
from z3c.indexer.interfaces import IIndex
from z3c.indexer.indexer import ValueIndexer

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent

from quotationtool.bibliography.interfaces import IEntry


class TypeValueIndexer(ValueIndexer):
    """ Indexer for the 'type-field' index."""

    zope.component.adapts(IEntry)

    indexName = 'type-field'

    value = u'quotationtool.bibliography.interfaces.IEntry'


class IdValueIndexer(ValueIndexer):
    """ Indexer for the 'id-field' index."""
    
    zope.component.adapts(IEntry)

    indexName = 'id-field'
    
    @property
    def value(self):
        return self.context.__name__


def createBibliographyIndices(site):

    sm = site.getSiteManager()
    default = sm['default']

    author_field = default['author-field'] = FieldIndex()
    sm.registerUtility(author_field, IIndex, name='author-field')

    author_fulltext = default['author-fulltext'] = TextIndex()
    sm.registerUtility(author_fulltext, IIndex, name='author-fulltext')

    title_field = default['title-field'] = FieldIndex()
    sm.registerUtility(title_field, IIndex, name='title-field')

    title_fulltext = default['title-fulltext'] = TextIndex()
    sm.registerUtility(title_fulltext, IIndex, name='title-fulltext')

    year_field = default['year-field'] = FieldIndex()
    sm.registerUtility(year_field, IIndex, name='year-field')

    year_value = default['year-value'] = ValueIndex()
    sm.registerUtility(year_value, IIndex, name='year-value')

    if not default.has_key('any-fulltext'):
        any_fulltext = default['any-fulltext'] = TextIndex()
        sm.registerUtility(any_fulltext, IIndex, name='any-fulltext')


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createBibliographyIndicesSubscriber(event):
    """ Create indices when a new quotationtool site is created."""

    createBibliographyIndices(event.object)
