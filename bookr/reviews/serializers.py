from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Book, BookContributor, Contributor, Publisher, Review
from .utils import average_rating

# We must create the `PublisherSerializer` to serialize the `publisher` field
# in the `Book` model.
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'website', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class ReviewSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['content', 'rating', 'date_created', 'date_edited', 'creator', 'book']


class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    rating = serializers.SerializerMethodField('book_rating')
    reviews = serializers.SerializerMethodField('book_reviews')

    def book_rating(self, book):
        reviews = book.review_set.all()
        if reviews:
            return average_rating([review.rating for review in reviews])

    def book_reviews(self, book):
        reviews = book.review_set.all()
        if reviews:
            return ReviewSerializer(reviews, many=True).data

    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'publisher', 'rating', 'reviews']


class ContributionSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookContributor
        fields = ['book', 'role']


class ContributorSerializer(serializers.ModelSerializer):
    bookcontributor_set = ContributionSerializer(many=True, read_only=True)
    contribution_count = serializers.ReadOnlyField()

    class Meta:
        model = Contributor
        fields = [
            'first_names',
            'last_names',
            'email',
            'bookcontributor_set',
            'contribution_count',
        ]
