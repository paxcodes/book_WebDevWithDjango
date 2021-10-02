from django import template

from ..models import Review

register = template.Library()


@register.inclusion_tag('reviews/book_list.html')
def book_list(username: str):
    reviews = Review.objects.filter(creator__username=username)
    book_list = [review.book.title for review in reviews]
    return {'books_reviewed': book_list}
