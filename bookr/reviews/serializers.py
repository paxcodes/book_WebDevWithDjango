from rest_framework import serializers

from .models import Book, Publisher


# We must create the `PublisherSerializer` to serialize the `publisher` field
# in the `Book` model.
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'website', 'email']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'publisher']
