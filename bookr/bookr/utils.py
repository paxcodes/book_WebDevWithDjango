from datetime import datetime

from django.db.models import Count
from reviews.models import Review


def get_books_reviewed_by_month(username: str):
    """Get the books read by the user on per month basis.

    Args:
        username (str): The username for which the books needs to be returned.

    Returns:
        A dictionary of books read, with months as keys.
    """
    current_year = datetime.now().year
    return (
        # Filter the review records to choose all the records that belong to the
        # current user as well as the current year.
        Review.objects.filter(
            creator__username=username, date_created__year=current_year
        )
        # Select only the month field from the date_created attribute of the
        # Review model
        .values('date_created__month')
        # Select the total number of books read in a given month.
        .annotate(book_count=Count('book__title'))
    )
