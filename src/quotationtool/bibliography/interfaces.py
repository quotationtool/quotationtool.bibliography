# -*- coding: utf-8 -*-

import re
import zope.interface
import zope.schema
from zope.container.interfaces import IContainer, IContained
from zope.container.constraints import contains, containers
from zope.interface.common.interfaces import IException
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager


_ = MessageFactory('quotationtool')


NAMES_SEPARATOR = u" / "


class IEntryKey(zope.interface.Interface):
    pass


class EntryKey(zope.schema.TextLine):
    """ A bibtex entry key.

    Should this better be derived from zope.schema.ASCII?
    
        >>> from quotationtool.bibliography.interfaces import EntryKey
        >>> ref = EntryKey(title = u"Reference")
        >>> ref.validate(u'Adelung')
        >>> ref.validate(u'Adelung.')
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: Adelung.

        >>> ref.validate(u'Lück')
        Traceback (most recent call last):
        ...
        ConstraintNotSatisfied: ...


    """
    
    zope.interface.implements(IEntryKey)

    def constraint(self, value):
        return re.compile("^([a-zA-z0-9]|-|_|:)+$").match(value)


class IEntry(IContained):
    """ An entry in the bibliography. This is a base interface and all
    more specific entry types should be derived from this.
    """

    __name__ = EntryKey(
        title = _('ientry-name-title',
                  u"Database Key"),
        description = _('ientry-name-desc',
                        u"The unique key of the entry in the database. Typically this should be of the form &lt;name&gt;&lt;year&gt;&lt;counting letter&gt;, e.g. Adelung1808b."),
        required = True,
        #readonly = True,
        )
    

class IBibliography(zope.interface.Interface):
    """ A bibliography holding IEntry objects. This is the
    schema part of the bibliography."""
    

class IBibliographyContainer(IContainer):
    """ A bibliography is a container for IEntry objects. This
    interface and IBibliography must be different because of managing
    permissions."""
    
    contains('.IEntry')


class IConfiguration(zope.interface.Interface):
    """ Stores some configuration values. """
    
    language = zope.schema.Choice(
        title = _('',
                  u"Language"),
        description = _('',
                        u"The default language of the bibliography"),
        required = True,
        vocabulary = 'quotationtool.bibliography.Languages',
        default = 'english',
        )

    languages = zope.schema.Tuple(
        title = _('',
                  u"Available Languages"),
        description = _('',
                        u"All languages in that the formatted bibliography entries will be available to the user."),
        required = True,
        value_type = zope.schema.Choice(
            title = _('',
                      u"Language"),
            required = True,
            vocabulary = 'quotationtool.biblatex.Languages',
            default = 'english',
            ),
        default = ('english',),
        )


class IBibliographyCatalog(zope.interface.Interface):
    """A catalog of indexes that we want to search for in the
    bibliography."""

    any = zope.schema.TextLine(
        title = _('catalog-any-title',
                  u"Any field / free"),
        description = _('catalog-any-desc',
                        u"Free text."),
        required = False,
        default = u'',
        )

    author = zope.schema.TextLine(
        title = _('ibibliographycatalog-author-title',
                  u"Author / Editor"),
        description = _('ibibliographycatalog-author-desc',
                        u"Search by author or editor."),
        required = False,
        default = u'',
        )

    title = zope.schema.TextLine(
        title = _('ibibliographycatalog-title-title',
                  u"Title / Uniform Title"),
        description = _('ireferenceindexercatalog-title-desc',
                        u"Search by title or uniform title."
                        ),
        required = False,
        default = u'',
        )

    post = zope.schema.Int(
        title = _('ibibliographycatalog-post-title',
                  u"Published/Written After"),
        description = _('ibibliographycatalog-post-desc',
                  u"Matches, if published after."),
        required = False,
        )

    ante = zope.schema.Int(
        title = _('ibibliographycatalog-ante-title',
                  u"Published/Writter Before"),
        description = _('ibibliographycatalog-ante-desc',
                  u"Matsches, if published before."),
        required = False,
        )

    year = zope.schema.Int(
        title = _('ibibliographycatalog-year-title',
                  u"Year first published"),
        description = _('ibibliographycatalog-year-desc',
                  u"Matches the exact year of origin."),
        required = False,
        )

    language = zope.schema.TextLine(
        title = _('ibibliographycatalog-language-title',
                  u"Language / Original Language"),
        description = _('ibibliographycatalog-language-desc',
                  u"Search for items by language."),
        required = False,
        default = u'',
        )

    edition_year = zope.schema.TextLine(
        title = _('irefenceindexer-editionyear-title',
                  u"Year of edition"),
        description = _('ibibliographycatalog-edtionyear-desc',
                  u"Matches the year of the edition."),
        required = True,
        )

    publisher = zope.schema.TextLine(
        title = _('ibibliographycatalog-publisher-title',
                  u"Publisher"),
        description = _('ibibliographycatalog-publisher-desc',
                  u"Search by publisher."),
        required = False,
        default = u'',
        )

    location = zope.schema.TextLine(
        title = _('ibibliographycatalog-location-title',
                  u"Location"),
        description = _('ibibliographycatalog-location-desc',
                  u"Search by place of publication."),
        required = False,
        default = u'',
        )


class IAddEntryManager(IViewletManager):
    """ A viewlet manager that lets the user choose an entry type he
    wants to add.""" 
