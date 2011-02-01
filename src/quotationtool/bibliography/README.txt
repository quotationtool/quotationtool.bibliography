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
    ...     def __init__(self, author = u'', title = u'', year = u''):
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
    ...         return getattr(self.context, name)
    >>> zope.component.provideAdapter(MyCatalogAdapter)
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

