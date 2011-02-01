import zope.interface
import zope.component
from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import ISiteMenu
from z3c.menu.ready2go.manager import MenuManager

from quotationtool.skin.interfaces import ISubNavManager
from quotationtool.skin.browser.nav import MainNavItem


class IBibliographyMainNavItem(zope.interface.Interface): 
    """ A marker interface for the bibliography's item in the main navigation."""
    pass


class BibliographyMainNavItem(MainNavItem):
    """The bibliography navigation item in the main navigation."""

    zope.interface.implements(IBibliographyMainNavItem)


class IBibliographySubNav(ISubNavManager):
    """A manager for the bibliography subnavigation."""

BibliographySubNav = ViewletManager('bibliographysubnav',
                                    ISiteMenu,
                                    bases = (MenuManager,))

IBibliographySubNav.implementedBy(BibliographySubNav)


