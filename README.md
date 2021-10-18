# Web Development with Django

Django projects and apps created while going through the book "Web Development with Django" from Packt Publishing (February 2021).

The code from Packt Publishing or the authors is also in [GitHub](https://github.com/PacktPublishing/Web-Development-with-Django).

## Setting up Development Environment

The python version I used is 3.9.

1. `python -m venv --prompt "WebDevWithDjango" .venv`
2. `source .venv/bin/activate` [^1]
3. `pip install -r requirements.txt`

[^1]: If using Powershell, run `.venv\Scripts\Activate.ps1`. You may need to run `set-executionpolicy RemoteSigned` to allow scripts to run [[docs](http://technet.microsoft.com/en-us/library/ee176961.aspx)].

To setup the Bookr project,

1. Go to project directory, `cd bookr`
2. Run migrations, `python manage.py migrate`
3. Seed the database, `python manage.py loadcsv --csv reviews\management\commands\WebDevWithDjangoData.csv`
4. Run the server, `python manage.py runserver`
5. Create an admin, `python manage.py createsuperuser`
6. Setup regular user, `python manage.py changepassword marksandler@test.com`

