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
    TypeError: ('Could not adapt', <MyEntry object at 0x...>, <InterfaceClass quotationtool.bibliography.interfaces.IEntryKeyChooser>)

The name chooser adapts the entry to the IEntryKeyChooser interface
which defines a method called chooseKey(). So we have to provide an
adapter for our MyEntry class:

    >>> from quotationtool.bibliography import interfaces
    >>> class MyEntryKeyChooser(object):
    ...     zope.interface.implements(interfaces.IEntryKeyChooser)
    ...     zope.component.adapts(IMyEntry)
    ...     def __init__(self, context):
    ...         self.context = context
    ...	    def chooseKey(self):
    ...         rc = u""
    ...     	if self.context.author:
    ...		    rc += self.context.author[0].split(',')[0].strip()
    ...         if not rc and self.context.title:
    ...             rc += self.context.title
    ...         if self.context.year:
    ...             rc += str(self.context.year)
    ...         return rc
    >>> zope.component.provideAdapter(MyEntryKeyChooser)
    >>> interfaces.IEntryKeyChooser(mybook).chooseKey()
    u'Horkheimer1944'

Now we can use the namechooser:

    >>> names.chooseName(None, mybook)
    u'Horkheimer1944'

    >>> biblio[names.chooseName(None, mybook)] = mybook
    >>> #mybook.__name__
    u'Horkheimer1944'

    >>> names.chooseName(None, mybook)
    u'Horkheimer1944a'

    >>> mybook2 = MyEntry([u"von der Gruen, Max"], u"Vorstadtkrokodile", 1976)
    >>> names.chooseName(None, mybook2)
    u'vonderGruen1976'

As we can see, the name chooser removes whitespace from the name. All
non-ascii characters will be removed, too.

    >>> otherbook = MyEntry(title = u'Historisches W\\"{o}rterbuch der Philosophie', year = 1971)
    >>> names.chooseName(None, otherbook)
    u'HistorischesWorterbuchderPhilosophie1971'


We can also suggest a name. If the suggested name is already in use, the namechooser will automatically append an alphabetical suffix to make it unique:

    >>> names.chooseName(u'Horkheimer1944', mybook)
    u'Horkheimer1944a'

Suggesting a name overrides the key determined be the IEntryKeyChooser
adapter:

    >>> names.chooseName(u'Horkheimer1944', mybook2)
    u'Horkheimer1944a'


