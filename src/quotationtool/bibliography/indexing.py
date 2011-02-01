import zope.interface
import zope.component
import zc.catalog
from zope.catalog.text import TextIndex
from zc.catalog.catalogindex import ValueIndex

from zope.catalog.interfaces import ICatalog
import BTrees

import interfaces
from quotationtool.site.interfaces import INewQuotationtoolSiteEvent


def createBibliographyCatalogIndices(cat, interface = interfaces.IBibliographyCatalog):
    """Add indexes to the catalog passed in."""

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

    sm.registerUtility(cat, ICatalog,
                       name = 'bibliography')
