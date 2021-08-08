from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


class BookrAdminSite(admin.AdminSite):
    title_hader = 'Bookr Admin'
    site_header = 'Bookr administration'
    index_title = 'Bookr site admin'


class BookrAdminConfig(AdminConfig):
    default_site = 'bookr.admin.BookrAdminSite'
