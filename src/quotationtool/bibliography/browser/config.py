from zope.viewlet.manager import ViewletManager, WeightOrderedViewletManager
from z3c.pagelet.browser import BrowserPagelet


from quotationtool.bibliography import interfaces


class ConfigPagelet(BrowserPagelet):
    """ Configure the bibliography."""


ConfigManager = ViewletManager('bibliography_configuration',
                               interfaces.IConfigurationManager,
                               bases = (WeightOrderedViewletManager,))
