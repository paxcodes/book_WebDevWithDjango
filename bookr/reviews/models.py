from django.db import models
from django.contrib import auth


class Publisher(models.Model):
    """A company that publishes books."""

    name = models.CharField(max_length=50, help_text="The name of the Publisher.")
    website = models.URLField(help_text="The publisher's website.")
    email = models.EmailField(help_text="The publisher's email address.")

    def __str__(self) -> str:
        return self.name


class Contributor(models.Model):
    """A contributor to a book, e.g. author, editor, co-author."""

    first_names = models.CharField(
        max_length=50, help_text="The contributor's first name or names."
    )
    last_names = models.CharField(
        max_length=50, help_text="The contributor's last name or names."
    )
    email = models.EmailField(help_text="The contact email for the contributor.")

    def __str__(self):
        return self.initialed_name

    @property
    def initialed_name(self):
        """Name of contributor with only first names' initials. E.g. Pax, RW"""
        fn_initials = ''.join(name[0] for name in self.first_names.split(' '))
        return f"{self.last_names}, {fn_initials}"

    @property
    def full_name(self):
        """Full name of contributor. E.g. Williams, Pax"""
        return f"{self.last_names}, {self.first_names}"


class Book(models.Model):
    """A published book."""

    title = models.CharField(max_length=70, help_text="The title of the book.")
    publication_date = models.DateField(verbose_name="Date the book was published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")

    ### RELATIONSHIPS
    # Since `publisher` is a non-nullable ForeignKey, it is mandatory to pass.
    # `contributors`, on the other hand, are not mandatory.
    # Book.objects.create(
    #   title="Cracking the Code",
    #   publication_date=date(2012, 11, 21),
    #   isbn="7537334534243",
    #   publisher=some_publisher_object
    # )
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(Contributor, through='BookContributor')

    def isbn13(self):
        """Format isbn with hyphens."""
        return f"{self.isbn[0:3]}-{self.isbn[3:4]}-{self.isbn[4:6]}-{self.isbn[6:12]}-{self.isbn[12:13]}"

    def __str__(self) -> str:
        return self.title


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this contributor had in the book.",
        choices=ContributionRole.choices,
        max_length=20,
    )


class Review(models.Model):
    content = models.TextField(help_text="The review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the review was created."
    )
    date_edited = models.DateTimeField(
        null=True, help_text="The date and time the review was last edited."
    )

    # `auth.get_user_model()` refers to the `User` model from Django's built-in
    # authentication module.
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="The book that this review is for."
    )
