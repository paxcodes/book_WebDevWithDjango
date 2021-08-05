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

`python manage.py migrate`
