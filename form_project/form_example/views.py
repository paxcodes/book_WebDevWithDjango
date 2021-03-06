from django.shortcuts import redirect, render

from .forms import OrderForm


def form_example(request):
    initial_data = {"email": "user@example.com"}
    form = (
        OrderForm(request.POST, initial=initial_data)
        if request.method == "POST"
        else OrderForm(initial=initial_data)
    )

    if form.is_valid():
        # cleaned_data is only populated if the form is valid
        for name, value in form.cleaned_data.items():
            print(f"{name}: ({type(value)}) {value}")
        # Redirect to a success page according to page 325
        return redirect("/success-page/")

    return render(
        request, "form-example.html", {"method": request.method, "form": form}
    )


# View function for the success page (according to page 325)
def form_success(request):
    return render(request, "form-success.html")
