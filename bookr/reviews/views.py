from django.http import HttpResponse

from .models import Book

def welcome_view(request):
    message = f"<html><h1>Welcome to Bookr!</h1> Something more her {Book.objects.count()}</html>"
    return HttpResponse(message)
