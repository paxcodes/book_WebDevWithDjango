from django.contrib import admin

from reviews.models import Publisher, Contributor, Book, BookContributor, Review


def initialed_name(contributor):
    """Name of contributor with only first names' initials. E.g. Pax, RW"""
    fn_initials = ''.join(name[0] for name in contributor.first_names.split(' '))
    return f"{contributor.last_names}, {fn_initials}"


class ContributorAdmin(admin.ModelAdmin):
    list_display = (initialed_name,)


class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13', 'publication_date', 'publisher')
    list_filter = ['publisher', 'publication_date']

    # You can also do "dunder" matches like `__exact` `__startswith`
    # E.g. isbn__exact will require the complete ISBN to be matched.
    search_fields = ('title', 'isbn', 'publisher__name')


class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('creator', 'book')}),
        ('Review content', {'fields': ('content', 'rating')}),
    )


admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)
