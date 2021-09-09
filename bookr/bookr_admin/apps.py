from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


# The AdminConfig class is used to define the application that should be used as a
# default admin site, and also to override the default behaviour of the Django
# admin site.
class BookrAdminConfig(AdminConfig):
    default_site = 'bookr_admin.admin.BookrAdmin'
