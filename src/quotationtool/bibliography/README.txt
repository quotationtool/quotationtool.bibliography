name chooser
============

There is a namechooser component that cooks the names of the entries
in the bibliography. The name chooser component is an adapter to the
bibliography.

    >>>	from quotationtool.bibliography.namechooser import EntryNameChooser
    >>> from quotationtool.bibliography.bibliography import Bibliography
    >>> biblio = Bibliography()
    >>> names = EntryNameChooser(biblio)
    >>> names.context == biblio
    True

We want to choose names for an entry. So we need an entry type.

    >>> import zope.interface
    >>> import zope.component
    >>> class IMyEntry(zope.interface.Interface): pass
    >>> class MyEntry(object):
    ...     zope.interface.implements(IMyEntry)
    ...     __name__ = __parent__ = None
    ...     def __init__(self, author = [], title = u'', year = None):
    ...         self.author = author
    ...         self.title = title
    ...         self.year = year

    >>> mybook = MyEntry([u"Horkheimer, Max", u"Adorno, Theodor W."], u"Dialektik der ..", 1944)

    >>> names.chooseName(None, mybook)
    Traceback (most recent call last):
    TypeError: ('Could not adapt', <MyEntry object at 0x...>, <InterfaceClass quotationtool.bibliography.interfaces.IBibliographyCatalog>)

The name chooser adapts the entry to the IBibliographyCatalog
interface where author, title and year fields are given. So we have to
provide an adapter for our MyEntry class:

    >>> from quotationtool.bibliography import interfaces
    >>> class MyCatalogAdapter(object):
    ...     zope.interface.implements(interfaces.IBibliographyCatalog)
    ...     zope.component.adapts(IMyEntry)
    ...     def __init__(self, context):
    ...         self.context = context
    ...     def getter(self, attr):
    ...         return getattr(self.context, attr, u"")
    ...     def __getattr__(self, name):
    ...	    	if name == 'author':
    ...		    rc = u""
    ...             for au in getattr(self.context, 'author', []):
    ...		        rc += au +u", "
    ...		    return rc
    ...         return getattr(self.context, name, u"")
    >>> zope.component.provideAdapter(MyCatalogAdapter)
    >>> interfaces.IBibliographyCatalog(mybook).author
    u'Horkheimer, Max, Adorno, Theodor W., '

Now we can use the namechooser:

    >>> names.chooseName(None, mybook)
    u'Horkheimer1944'

    >>> biblio[names.chooseName(None, mybook)] = mybook
    >>> mybook.__name__
    u'Horkheimer1944'

    >>> names.chooseName(None, mybook)
    u'Horkheimer1944a'

    >>> mybook2 = MyEntry([u"von der Gruen, Max"], u"Vorstadtkrokodile", 1976)
    >>> names.chooseName(None, mybook2)
    u'vonderGruen1976'


    >>> otherbook = MyEntry(title = u'Historisches W\\"{o}rterbuch der Philosophie', year = 1971)
    >>> names.chooseName(None, otherbook)
    u'HistorischesWorterbuchderPhilosophie1971'


We can also suggest a name:

    >>> names.chooseName(u'Horkheimer1944', mybook)
    u'Horkheimer1944a'

Suggesting a name may be stupid, but the name chooser answers:

    >>> names.chooseName(u'Horkheimer1944', mybook2)
    u'Horkheimer1944a'


Indexing
--------

In order to get the values out of an entry object we make use of
adapters. We use the same adapter as above, which is still registered.

Create the catalog:

    >>> from quotationtool.bibliography.indexing import createBibliographyCatalogIndices, filter
    >>> from zc.catalog.extentcatalog import FilterExtent, Catalog
    >>> extent = FilterExtent(filter)
    >>> cat = Catalog(extent)
    >>> createBibliographyCatalogIndices(cat)
    >>> list(cat.keys())
    [u'ante', u'author', u'language', u'post', u'title', u'year']

    >>> cat.index_doc(1, mybook)
    >>> assert(len(extent) == 1)
    Traceback (most recent call last):
    ...
    AssertionError

The filter is passed by objects that implement interfaces.IEntry
only. So if we want to get our MyBook objects indexed we have to
provide this interface.

    >>> from zope.interface import classImplements
    >>> classImplements(MyEntry, interfaces.IEntry)
    >>> cat.index_doc(1, mybook)
    >>> assert(len(extent) == 1)

Now we can search the indices:

    >>> list(cat.apply({'author': u"mendelssohn"}))
    []

    >>> list(cat.apply({'author': u"horkheimer"}))
    [1]

    >>> list(cat.apply({'author': u"adorno"}))
    [1]

    >>> list(cat.apply({'title': u"dialektik"}))
    [1]

    >>> cat.index_doc(2, mybook2)
    >>> list(cat.apply({'author': u"gruen"}))
    [2]

    >>> list(cat.apply({'author': u"max"}))
    [1, 2]
