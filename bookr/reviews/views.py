from django.shortcuts import render


def index(request):
    return render(request, "base.html")


def book_search_results(request):
    search = request.GET.get("search", "")
    # TODO handle if search is an empty string
    return render(request, "search-results.html", {"search_keywords": search})
