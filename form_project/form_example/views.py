from django.shortcuts import redirect, render

from .forms import ExampleForm


def form_example(request):
    # Ex 6.2: Print out the received POST data
    for name in request.POST:
        print(f"{name}: {request.POST.getlist(name)}")

    form = ExampleForm(request.POST) if request.method == "POST" else ExampleForm()
    if form.is_valid():
        return redirect("/success-page/")

    return render(
        request, "form-example.html", {"method": request.method, "form": form}
    )


def form_success(request):
    return render(request, "form-success.html")
