from core.models import Tenant, Organization, Department, Customer
from django.contrib import admin

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        # Pobierz listę aplikacji
        app_list = super().get_app_list(request)

        # Znajdź aplikację "core" i ustaw kolejność modeli
        for app in app_list:
            if app['app_label'] == 'core':
                app['models'].sort(key=lambda x: [
                    'Tenant', 'Organization', 'Department', 'Customer'
                ].index(x['object_name']))
        return app_list


custom_admin_site = CustomAdminSite(name='custom_admin')

custom_admin_site.register(Tenant)
custom_admin_site.register(Organization)
custom_admin_site.register(Department)
custom_admin_site.register(Customer)

custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)