from django.shortcuts import render


def index(request):
    names = "john,doe,mark,swain"
    return render(request, "index.html", {"names": names})


def greeting(request):
    books = {"The night rider": "Ben Author", "The Justice": "Don Abeman"}
    return render(
        request, "simple_tag_template.html", {"username": 'jdoe', 'books': books}
    )
