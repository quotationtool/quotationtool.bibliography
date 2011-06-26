import zope.interface
import zope.component
from zope.app.component.hooks import getSite

import interfaces
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent

from z3c.indexer.index import TextIndex, ValueIndex, FieldIndex

def createBibliographyIndices(site=getSite(), prefix=''):
    """ Create some indices for searching the bibliography."""
    
    sm = site.getSiteManager()

    if not prefix+'any_index' in sm['default']:
        sm['default'][prefix+'any_index'] = any_index = TextIndex()
        sm.registerUtility(any_index, IIndex, prefix+'author_textindex')

    sm['default'][prefix+'author_textindex'] = author_textindex = TextIndex()
    sm.registerUtility(author_textindex, IIndex, prefix+'author_textindex')

    sm['default'][prefix+'author_index'] = author_index = FieldIndex()
    sm.registerUtility(author_index, IIndex, prefix+'author_index')

    sm['default'][prefix+'title_textindex'] = title_textindex = TextIndex()
    sm.registerUtility(title_textindex, IIndex, prefix+'title_textindex')

    sm['default'][prefix+'title_index'] = title_index = FieldIndex()
    sm.registerUtility(title_index, IIndex, prefix+'title_index')

    sm['default'][prefix+'post_year_index'] = post_year_index = FieldIndex()
    sm.registerUtility(post_year_index, IIndex, prefix+'post_year_index')

    sm['default'][prefix+'ante_year_index'] = ante_year_index = FieldIndex()
    sm.registerUtility(ante_year_index, IIndex, prefix+'ante_year_index')

    sm['default'][prefix+'language_index'] = language_index = SetIndex()
    sm.registerUtility(language_index, IIndex, prefix+'language_index')
    

@zope.component.adapter(INewQuotationtoolSiteEvent)
def createBibliographyIndicesSubscriber(event):
    """ Create indices when a new quotationtool site is created."""
    createBibliographyIndices(event.object)





#BBB
import zc.catalog
from zope.catalog.text import TextIndex
from zc.catalog.catalogindex import ValueIndex

from zope.catalog.interfaces import ICatalog

def createBibliographyCatalogIndices(cat, interface = interfaces.IBibliographyCatalog):
    """Add indexes to the catalog passed in."""

    # we do not create the any index here!
    #cat['any'] = TextIndex(
    #    interface = interface,
    #    field_name = 'any')
    
    cat['author'] = TextIndex(
        interface = interface,
        field_name = 'author')
    
    cat['title'] = TextIndex(
        interface = interface,
        field_name = 'title')

    cat['post'] = ValueIndex(
        interface = interface,
        field_name = 'post')

    cat['ante'] = ValueIndex(
        interface = interface,
        field_name = 'ante')

    cat['year'] = ValueIndex(
        interface = interface,
        field_name = 'year')

    cat['language'] = ValueIndex(
        interface = interface,
        field_name = 'language')
        

def filter(extent, uid, obj):
    assert zc.catalog.interfaces.IFilterExtent.providedBy(extent)
    return interfaces.IEntry.providedBy(obj)


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createBibliographyCatalog(event):
    """ Create a bibliography catalog when a new quotationtool site is
    created."""
    
    sm = event.object.getSiteManager()

    from zc.catalog.extentcatalog import FilterExtent, Catalog
    extent = FilterExtent(filter)#, family = BTrees.family64)

    sm['default']['bibliography_catalog'] = cat = Catalog(extent)

    createBibliographyCatalogIndices(cat)

    cat['any'] = TextIndex(
        interface = interfaces.IBibliographyCatalog,
        field_name = 'any')

    sm.registerUtility(cat, ICatalog,
                       name = 'bibliography')

