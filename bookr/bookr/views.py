from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from plotly.offline import plot
from plotly import graph_objects as graphs

from .utils import get_books_reviewed_by_month, get_xlsx_data_list_of_books_reviewed


@login_required
def profile(request):
    user = request.user
    permissions = user.get_all_permissions()
    # Get the books reviewed in different months this year
    books_by_month = get_books_reviewed_by_month(user.username)
    # Initialize the Axis for graphs, X-Axis is months, Y-axis is books read.
    # Since `books_by_month` only contain months that actually have values,
    # we initialize all `books_read` for every month to 0.
    months = [i + 1 for i in range(12)]
    books_read = [0 for _ in range(12)]
    # Set the value for books read per month on Y-Axis
    for num_books_read in books_by_month:
        list_index = num_books_read['date_created__month'] - 1
        books_read[list_index] = num_books_read['book_count']

    # Generate a scatter plot HTML
    figure = graphs.Figure()
    scatter = graphs.Scatter(x=months, y=books_read)
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title="Month", yaxis_title="No. of books read")
    plot_html = plot(figure, output_type='div')

    return render(
        request,
        'profile.html',
        {'user': user, 'permissions': permissions, 'books_read_plot': plot_html},
    )


@login_required
def download_user_book_data(request):
    xlsx_data = get_xlsx_data_list_of_books_reviewed(request.user.username)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=books_reviewed.xlsx'
    response.write(xlsx_data)
    return response
