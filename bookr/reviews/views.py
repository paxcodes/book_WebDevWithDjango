from io import BytesIO

from django.core.files.images import ImageFile
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils import timezone
from PIL import Image

from .models import Book, Publisher, Review
from .utils import average_rating
from .forms import BookMediaForm, SearchForm, PublisherForm, ReviewForm
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
                messages.success(
                    request, f'Publisher "{updated_publisher}" was created.'
                )
            else:
                messages.success(
                    request, f'Publisher "{updated_publisher}" was updated.'
                )
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(
        request,
        "reviews/instance-form.html",
        {"form": form, "model_type": "Publisher", "instance": publisher},
    )


def review_edit(request, book_pk, review_pk=None):
    # sourcery skip: extract-method
    book = get_object_or_404(Book, pk=book_pk)
    review = (
        get_object_or_404(Review, book_id=book_pk, pk=review_pk) if review_pk else None
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            new_or_updated_review = form.save(commit=False)
            new_or_updated_review.book = book
            if review:
                new_or_updated_review.date_edited = timezone.now()
            new_or_updated_review.save()
            action = "updated" if review else "created"
            messages.success(request, f'Review for "{book.title}" was {action}.')
            return redirect("book_details", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/instance-form.html",
        {
            "form": form,
            "model_type": "Review",
            "instance": review,
            "related_model_type": "Book",
            "related_instance": book,
        },
    )


def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            if cover := form.cleaned_data['cover']:
                image = Image.open(cover)
                image.thumbnail((300, 300))
                # Use BytesIO for file-like objects that only exist in memory.
                # See section "Writing PIL images to ImageField" for more info.
                # Doing it this way will prevent having to write the image into disk
                # twice, making the process slower. Rather, the image is written in
                # memory, processed, then written to disk.
                image_data = BytesIO()
                # Writes the thumbnail to the image_data (an in-memory object)
                image.save(fp=image_data, format=cover.image.format)
                # Wrap the BytesIO containing the image data into an object the Django
                # API can interact with. ImageFile is from `django.core.files.images`
                image_file = ImageFile(image_data)
                # TODO Clarify what this actually does. Posted an issue in GitHub
                # https://github.com/PacktPublishing/Web-Development-with-Django/issues/10
                # Save the image to disk?
                book.cover.save(cover.name, image_file)
            book.save()
            messages.success(request, f"Book {book} was successfully updated.")
            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)

    return render(
        request,
        "reviews/instance-form.html",
        {"instance": book, "form": form, "model_type": "Book", "is_file_upload": True},
    )
