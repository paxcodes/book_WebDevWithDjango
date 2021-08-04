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

## Cheatsheet

Quick reference of commands I encountered while going through the book:

`django-admin startproject [PROJECT_NAME]`

`python manage.py runserver`

`python manage.py startapp [APP_NAME]`


