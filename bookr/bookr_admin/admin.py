from django.template.response import TemplateResponse
from django.urls import path
from django.contrib import admin


class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Administration"
    site_title = "Bookr Administration"
    index_title = "Bookr Administration"
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
        return TemplateResponse(request, "admin/profile.html", context)

    def get_urls(self):
        """Overrides the AdminSite.get_urls() method."""
        urls = super().get_urls()
        # To make sure that this view is only accessible to the logged-in admins, wrap
        # `self.profile_view` with `self.admin_view()`. The `AdminSite.admin_view()
        # method causes the view to be restricted to those users who are logged in.
        # If a user who is currently not logged into the admin site tries to visit the
        # URL directly, they will get redirected to the login page, and only in the
        # event of a successful login will they be allowed to see the contents of our
        # custom page.
        url_patterns = [path("profile", self.admin_view(self.profile_view))]
        return urls + url_patterns
