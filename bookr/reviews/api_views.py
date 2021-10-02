from rest_framework import generics
from rest_framework.response import Response

from .models import Book, Contributor
from .serializers import BookSerializer, ContributorSerializer


class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AllContributors(generics.ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
