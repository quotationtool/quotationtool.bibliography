from zope.container.contained import NameChooser
import zope.interface
import zope.component

from quotationtool.bibliography import interfaces


class EntryNameChooser(NameChooser):
    """ A component that tries to choose an entry key (unique name)
    for a bibliography entry.
    """

    zope.interface.implements(zope.container.interfaces.INameChooser)
    zope.component.adapts(interfaces.IBibliography)

    def chooseName(self, name, obj):
        def removeNonAscii(s): 
            return "".join(i for i in s if ((ord(i)>=48 and ord(i)<=57) or 
                                            (ord(i)>=65 and ord(i)<=90) or
                                            (ord(i)>=97 and ord(i)<=122) or
                                            i in (':', '_', '-')))
        if not name:
            name = interfaces.IEntryKeyChooser(obj).chooseKey()
            if not name:
                raise Exception("Neither 'name' argument given nor IEntryKeyChooser gave a name.")
        name = removeNonAscii(name)
        if name not in self.context:
            return name
        # append alphabetic suffix 'a', 'b', ... or 'z'.
        for i in range(25):
            if  not name + chr(97 + i) in self.context:
                return name + chr(97 + i)
        raise Exception("No name found!")
