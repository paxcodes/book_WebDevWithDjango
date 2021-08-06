# Notes

Things I learned and caught me by surprise.

## Chapter 1: Introduction to Django

### Scaffolding a Django Project and App: Repetitive Folder Names

It seems like it's "normal" for Django projects to have "repetitive" folder names. As seen in [Packt's GitHub's final folder](https://github.com/PacktPublishing/Web-Development-with-Django/tree/master/Chapter18/final), the directory structure is like this: 

```
- final/
  - bookr/
    - bookr/
        - __init__.py
        - asgi.py
        - settings.py
        - [etc.]
    - manage.py
    - [etc.]
    - requirements.txt
```

And if your top-level directory name is also `bookr` instead of `final`, that would mean `bookr` is repeated 3 times.

### ❓ Apps can have their own apps?

When I created an app `reviews` under the `bookr` project, under `reviews` folder, I saw `apps.py`. Does that means apps can have their own apps (sub-applications) that is created / behaves _the same way_ as an app _directly under the Django project_?

### Registering Templates

> Many options are available to tell Django how to find templates, which can be set in the TEMPLATES setting of settings.py but the easiest one (for now ) is to create a `templates` directory inside the `reviews` directory. Django will look in this and other apps' templates directories* because `APP_DIRS` being True in the `settings.py` file... (p. 46)

\* That is, it will look in *registered* apps' templates directories. You _register_ an app by adding it in the `INSTALLED_APPS` list.

## Cheatsheet

Quick reference of commands I encountered while going through the book:

`django-admin startproject [PROJECT_NAME]`

`python manage.py runserver`

`python manage.py startapp [APP_NAME]`

### Database + Migrations

`python manage.py migrate`

`python manage.py makemigrations [optional:APP_NAME]` | Without the `APP_NAME`, Django will create migration scripts for all apps.

`python manage.py showmigrations` | Show migration status (whether a script has been run or not).

`python manage.py sqlmigrate [APP_NAME] [MIGRATION_SCRIPT]` |  Shows the SQL command equivalent used when Django runs the migration script.

`python manage.py shell`

### CRUD Operations

Code below assumes the following imports,
```py
from reviews.models import Publisher, Book, Contributor, BookContributor
from datetime import date
```

#### `Create` Operations

```py
##
## Basically 2 methods: `save()` OR `create()`
##
# Option 1: Instantiate model, then save()
publisher1 = Publisher(
    name="No Starch Press",
    website="https://www.nsp.com",
    email="info@nsp.com",
)
publisher1.save()

# Option 2: Use `create`
publisher2 = Publisher.objects.create(
    name="Manning",
    website="https://www.manningbooks.com",
    email="info@manning.com",
)
contributor1 = Contributor.objects.create(
    first_names="Jeconiah", last_names="Williams", email="jewilliams@flankroutes.com"
)

##
## Creating objects with "Foreign Key" relationships
#  e.g. Book has one publisher: Use `save()` or `create()`
##
book2 = Book(
    title="The Slackers",
    publication_date=date(2015, 12, 23),
    isbn="5673345",
    publisher=publisher2,
)
book2.save()

book1 = Book.objects.create(
    title="Python Machine Learning",
    publication_date=date(2012, 11, 21),
    isbn="7537334534243",
    publisher=publisher1,
)

##
## Many-to-many relationships
##

# Using the intermediary model, BookContributor
# You can use `save()` like this,
book_contributor1 = BookContributor(book=book1, contributor=contributor1, role='AUTHOR')
book_contributor1.save()

# Or `create()`:
book_contributor1 = BookContributor.objects.create(
    book=book1, contributor=contributor1, role='AUTHOR'
)
# Using attribute's methods
# `add()` : Adds a single contributor, using an existing instance
contributor2 = Contributor.objects.create(
    first_names="Sean", last_names="Williams", email="sewilliams@flankroutes.com"
)
book1.contributors.add(contributor2, through_defaults={'role': 'EDITOR'})
# `create()` : Adds a single contributor, by creating an instance
book1.contributors.create(
    first_names="Pax",
    last_names="Williams",
    email="pawilliams@flankroutes.com",
    through_defaults={'role': 'EDITOR'},
)
# `set()` : Add multiple contributors
# ⚠️ This completely overrides data for an object. If there are already existing
# data (i.e. contributors), using `set` will REMOVE those existing contributors
# and add these new contributors.
co_author1 = Contributor.objects.create(
    first_names="Wendy", last_names="Williams", email="wewilliams@flankroutes.com"
)
co_author2 = Contributor.objects.create(
    first_names="Wayne", last_names="Williams", email="wawilliams@flankroutes.com"
)
book2.contributors.set([co_author1, co_author2], through_defaults={'role': 'CO_AUTHOR'})
book2.contributors.add(contributor2, through_defaults={'role': 'AUTHOR'})
```

#### `Read` Operations

```py
# A single record with `get()` using an attribute; Has to be an exact match
book_cracking_the_code = Book.objects.get(title="Cracking the Code")

# A single record with `get()` using `primary_key` attribute
book_with_pk_1 = Book.objects.get(pk=1)

# Multiple records with `all()`
all_the_books = Book.objects.all()
all_the_books[0].title  # First book object where you have full data access

# Multiple records with `all().values()` to get dictionaries instead of objects
all_the_books_dict = Book.objects.all().values()
all_the_books_dict[0]["title"]


# Records of many-to-many relationships using `all()`
# Use `contributors` attribute that's defined in the Book model to get all contributors
book_1_contributors = book_with_pk_1.contributors.all()

# Reverse lookup of many-to-many relationships
# Contributor `model` doesn't have a `book` attribute defined, but we can still get
# the books a contributor has contributed to by using `MODELNAME_set.all()`
contributor1.book_set.all()

# Sorting
contributors_by_last_name = Contributor.objects.order_by("last_names")
contributors_by_last_name_desc = Contributor.objects.order_by("-last_names")
contributors_by_names = Contributor.objects.order_by("last_names", "first_names")


##
## Filtering objects
##
# Exact Match | TODO Verify if exact match
Contributor.objects.filter(last_names="Macnab")
Contributor.objects.filter(last_names="Williams")
Contributor.objects.filter(last_names="Nobody")  # Empty QuerySet `<QuerySet []>`

# Field lookups: `ATTRIBUTE__COMPARISON-OP`
books_2012_onwards = Book.objects.filter(publication_date__gte=date(2013, 1, 1))
books_before_2012 = Book.objects.filter(publication_date__lt=date(2013, 1, 1))
# Other `COMPARISON-OP`: `lte`, `gt`

# Pattern matching: `ATTRIBUTE__PATTERNMATCHING-OP`
contributors_williams_family = Contributor.objects.filter(
    email__contains="williams@flankroutes.com"
)
# Other `PATTERNMATCHING-OP`: `icontains` for case-insensitive matching |
#   `startswith` to match any string starting with the specified string

# Using relationships: foreign keys | `FOREIGNKEY__ATTRIBUTE`
Book.objects.filter(publisher__name="Pocket Books")

# Using relationships: model name | `MODELNAME__ATTRIBUTE`
# We can use `get()` because a book has only one publisher
Publisher.objects.get(book__title="Cracking the Code")

# Using the object instance
book_cracking_the_code = Book.objects.get(title="Cracking the Code")
book_cracking_the_code.publisher

# Multiple filters
# TODO What is the difference between these two? Is chaining queries like this optimal?
Book.objects.filter(publisher__name__contains="Packt", title__contains="Crack")
Book.objects.filter(publisher__name__contains="Packt").filter(title__contains="Crack")


# Excluding
contributors_not_williams = Contributor.objects.exclude(last_names="Williams")
```

#### `Update` Operations

```py
# Option 1: Modify model instance attribute, then `save()`
publisher1.email = "customer.support@packtpub.com"
publisher1.save()

# Option 2: Using `update()`
Book.objects.filter(pk=1).update(title="Cracking the Coding Interview")
# `update()` is only present in `QuerySet`, not in objects. So, this will not work:
# `Book.objects.get(pk=1).update(...)`; It will give an error:
#   `AttributeError: 'Book' object has no attribute 'update'`
```

#### `Delete` Operation

```py
Contributor.objects.get(pk=1).delete()
```