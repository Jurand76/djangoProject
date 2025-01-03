"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import TenantViewSet, OrganizationViewSet, DepartmentViewSet, CustomerViewSet, homepage
from core.admin import custom_admin_site
from django.contrib.auth import views as auth_views
from core import views

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),  # Logout
    path('core/', include('core.urls')),
    #path('tenants/', views.tenant_list, name='tenant_list'),  # Tenants list
    #path('tenants/add/', views.add_tenant, name='add_tenant'),  # Adding tenants
    path('admin/', custom_admin_site.urls),   # Admin site Django
    path('api/', include(router.urls)),        # API from core.urls
]
