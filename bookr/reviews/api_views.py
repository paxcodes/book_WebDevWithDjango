from django.contrib.auth import authenticate
from rest_framework import viewsets, status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


class Login(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if not user:
            # There is an argument to be had for returning a 404, "Client posted with a
            # set of credentials that were NOT FOUND" although a strict RESTful API
            # would return a 403 or 401. See PySlacker comments and StackOverflow posts,
            # https://stackoverflow.com/questions/32752578
            # https://stackoverflow.com/questions/26093875
            return Response(
                {'error': 'Credentials are incorrect or user does not exist'},
                status=status.HTTP_404_NOT_FOUND,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# `ReadOnlyModelViewSet` ensures that the views are used for the GET operation only.
class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Assigning `TokenAuthentication` to authentication_classes property will require
    # users who wants to access this viewset to authenticate using token-based
    # authentication.
    authentication_classes = [authentication.TokenAuthentication]
    # Check to see if the given user has permission to view the data in this model.
    permissions_classes = [permissions.IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.order_by('-date_created')
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = []
