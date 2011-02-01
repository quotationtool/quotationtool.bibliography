from zope.container.contained import NameChooser
import zope.interface
import zope.component

from quotationtool.bibliography import interfaces


class EntryNameChooser(NameChooser):
    """ A component that tries to make a bibtex key for a bibliography
    entry.
    """

    zope.interface.implements(zope.container.interfaces.INameChooser)
    zope.component.adapts(interfaces.IBibliography)

    def chooseName(self, name, obj):
        def removeNonAscii(s): 
            return "".join(i for i in s if ((ord(i)>=48 and ord(i)<=57) or 
                                            (ord(i)>=65 and ord(i)<=90) or
                                            (ord(i)>=97 and ord(i)<=122) or
                                            i in (':', '_', '-')))
        if name:
            name = removeNonAscii(name)
            if name and name not in self.context:
                return name
            for i in range(25):
                if  not name + chr(97 + i) in self.context:
                    return name + chr(97 + i)
        # no success with proposed name
        obj = interfaces.IBibliographyCatalog(obj)
        name = u""
        if obj.author:
            name += removeNonAscii(obj.author[0].split(',')[0])
        else:
            if obj.title:
                name += removeNonAscii(obj.title)
    
        if getattr(obj, 'year', None):
            name += unicode(obj.year)
        else:
            if getattr(obj, 'ante', None):
                name += unicode(obj.ante)
            else:
                if getattr(obj, 'post', None):
                    name += unicode(obj.post)

        if not name in self.context:
            return name
        for i in range(25):
            if not name + chr(97 + i) in self.context:
                return name + chr(97 + i)
        raise Exception("No name found!")
