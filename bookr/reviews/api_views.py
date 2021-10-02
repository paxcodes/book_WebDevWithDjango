from rest_framework import generics
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
