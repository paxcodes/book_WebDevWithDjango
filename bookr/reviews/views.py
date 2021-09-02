from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import Book, Publisher
from .utils import average_rating
from .forms import SearchForm, PublisherForm
from .crud import books


def index(request):
    return render(request, "base.html")


def book_search(request):
    form = SearchForm(request.GET)
    # "The search should only be performed if the form is valid and contains
    # some search text"
    results = []
    if form.is_valid() and (search_text := form.cleaned_data.get("search", "")):
        results = books.search(
            attr=form.cleaned_data.get("search_in", "title"),
            search_text=search_text,
        )
    return render(
        request,
        "reviews/search-results.html",
        {"search_text": search_text, "form": form, "results": results},
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


def publisher_edit(request, pk=None):
    publisher = None if pk is None else get_object_or_404(Publisher, pk=pk)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, f"Publisher {updated_publisher} was created.")
            else:
                messages.success(request, f"Publisher {updated_publisher} was updated.")
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(
        request, "publisher-form.html", {"method": request.method, "form": form}
    )
