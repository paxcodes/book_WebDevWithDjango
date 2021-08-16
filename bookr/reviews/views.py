from django.shortcuts import get_object_or_404, render

from .models import Book
from .utils import average_rating
from .forms import SearchForm


def index(request):
    return render(request, "base.html")


def book_search(request):
    form = SearchForm(request.GET)
    # TODO do we still need the code below?
    search_text = request.GET.get("search", "")
    return render(
        request,
        "reviews/search-results.html",
        {"search_text": search_text, "form": form},
    )


def index(request):
    return render(request, 'base.html')

def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        book_rating = None
        number_of_reviews = 0
        if reviews := book.review_set.all():
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        book_list.append(
            {
                'book': book,
                'book_rating': book_rating,
                'number_of_reviews': number_of_reviews,
            }
        )
    context = {'book_list': book_list}
    return render(request, 'reviews/books_list.html', context)


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_rating = reviews = None
    if reviews := book.review_set.all():
        book_rating = '⭐️ ' * average_rating([review.rating for review in reviews])
        for review in reviews:
            # TODO Is there a way we can do this in the template itself?
            # Using a filter? Can't seem to find any in built-in filters
            review.pretty_rating = '⭐️ ' * review.rating
    context = {'book': book, 'book_rating': book_rating, 'reviews': reviews}
    return render(request, 'reviews/book_detail.html', context)
