from django.db.models import Q

from ..models import Book

# TODO replace magic strings with Enums / Types ?
def search(attr: str, search_text: str):
    result = []
    if attr == 'title':
        result = Book.objects.filter(title__icontains=search_text)
    elif attr == 'contributor':
        result = Book.objects.filter(
            Q(contributors__first_names__icontains=search_text)
            | Q(contributors__last_names__icontains=search_text)
        )
    return result
