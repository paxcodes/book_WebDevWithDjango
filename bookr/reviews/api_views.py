from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer

# `ReadOnlyModelViewSet` ensures that the views are used for the GET operation only.
class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.order_by('-date_created')
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = []
