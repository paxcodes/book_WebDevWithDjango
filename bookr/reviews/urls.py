from django.urls import path

from . import views, api_views

urlpatterns = [
    path('api/books/', api_views.all_books, name='all_books'),
    path('', views.index),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_details, name='book_details'),
    path('books/<int:pk>/media', views.book_media, name='book_media_edit'),
    path('books/<int:book_pk>/reviews/new/', views.review_edit, name='review_create'),
    path(
        'books/<int:book_pk>/reviews/<int:review_pk>/',
        views.review_edit,
        name='review_edit',
    ),
    path('books/search/', views.book_search, name="book_search"),
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publishers/new/', views.publisher_edit, name='publisher_create'),
]
