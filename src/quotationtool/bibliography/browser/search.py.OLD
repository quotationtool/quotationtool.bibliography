from quotationtool.search.browser import search

from quotationtool.bibliography.interfaces import _


class EntriesSearchTargetViewlet(search.SearchTargetViewlet):
    """ Let's the user choose bibliographic entries to search."""

    label = _('entries-search-target-label', 
              u"Bibliographic Entries")

    description = _('entries-search-target-description',
                    u"Search for a bibliographic entry by author/editor, title, year etc.")


class SearchForm(search.SearchFormBase):
    """ Search form for bibliography catalog."""

    catalog_name = 'bibliography'

    query = ('any', 'author', 'title', 'publisher', 'location', 'language',)

    label = _('bibliography-search-form-label',
              u"Search for bibliographic entries")


class SearchResultPage(search.SearchResultPageBase):
    """ Found items."""

    catalog_name = 'bibliography'

    def getEntries(self):
        return self.getResultPage()
