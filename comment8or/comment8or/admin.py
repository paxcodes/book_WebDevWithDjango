from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


class Comment8orAdminSite(admin.AdminSite):
    title_header = 'c8 site admin'
    index_title = 'c8admin'
    site_header = 'c8admin'
    # TODO is there a way to make path of the template explicit? Otherwise I am left
    # guessing where to find this template. (is it in the project? is it in the app?
    # base directory? I could look at settings.py but if there are multiple directories
    # listed there, how would I know right away where this is being pulled?)
    logout_template = 'admin/logged_out.html'


class Comment8orAdminConfig(AdminConfig):
    default_site = 'comment8or.admin.Comment8orAdminSite'
