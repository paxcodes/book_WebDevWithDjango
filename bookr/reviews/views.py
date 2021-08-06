from django.shortcuts import render

from .models import Book

def welcome_view(request):
    return render(request, "base.html")
