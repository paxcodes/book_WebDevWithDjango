from datetime import datetime
from io import BytesIO
from django.db.models.query import QuerySet

import xlsxwriter
from django.db.models import Count
from xlsxwriter.utility import remove_datetime_timezone
from reviews.models import Review


def get_books_reviewed_by_month(username: str):
    """Get the count of books reviewed by the user on per month basis.

    Args:
        username (str): The username for which the books needs to be returned.

    Returns:
        A dictionary of number of books reviewed, with months as keys.
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


def get_list_of_books_reviewed(username: str) -> QuerySet:
    """Get the list of books reviewed by { username }.

    Args:
        username (str): The user whose books reviewed we are fetching.

    Returns:
        A list of book objects / data.
    """
    # I have to manually list the attributes
    return Review.objects.filter(creator__username=username).values_list(
        'book__title', 'date_created', 'content'
    )


def write_data_to_xlsx(data: list) -> bytes:
    """Writes { data } to an xlsx file.

    Args:
        data (list): A list of objects

    Returns:
        bytes: Returns the xlsx data.
    """
    temp_file = BytesIO()
    workbook = xlsxwriter.Workbook(temp_file, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])
    workbook.close()
    return temp_file.getvalue()


def get_xlsx_data_list_of_books_reviewed(username: str) -> bytes:
    """Get list of books reviewed by { username } in .xlsx data format.

    Args:
        username (str): The user who created the reviews.

    Returns:
        bytes: xlsx data of list of books reviewed by { username }.
    """
    books = list(get_list_of_books_reviewed(username))
    books.insert(0, ("Book Title", "Review Content", "Review Date Created"))
    return write_data_to_xlsx(books)
