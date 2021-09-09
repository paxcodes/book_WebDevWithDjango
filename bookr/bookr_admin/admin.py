from django.template.response import TemplateResponse
from django.urls import path
from django.contrib import admin


class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Administration"
    logout_template = 'admin/logout.html'

    def profile_view(self, request):
        # This is required in order to allow Django's URL resolver inside the templates
        # to correctly resolve the view functions for an application.
        request.current_app = self.name
        # Fetch the template variables, which are required to render the contents, such
        # as site_title, site_header, and more, in the admin templates.
        # AdminSite.each_context() provides the dictionary of the admin site template
        # variables from the class.
        context = self.each_context(request)
        # Render the custom profile template when someone visits the URL endpoint
        # mapped to the custom view.
        return TemplateResponse(request, "admin/admin_profile.html", context)
