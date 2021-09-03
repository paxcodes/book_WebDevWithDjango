from django import forms

from .models import Publisher, Review


SEARCH_IN_CHOICES = (
    ("title", "Title"),
    ("contributor", "Contributor"),
)


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=SEARCH_IN_CHOICES)


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            "content",
            "rating",
            "creator",
        )
        # I could use the `exclude` property, like this:
        # exclude = ("book", "date_edited")
        # but whitelisting using `fields` property is more secure in case
        # we add a new field that shouldn't be editable and we forgot to exclude it.

    rating = forms.IntegerField(min_value=0, max_value=5)
