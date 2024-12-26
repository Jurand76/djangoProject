from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import TenantViewSet, OrganizationViewSet, DepartmentViewSet, CustomerViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.contrib.auth import views as auth_views
from core import views

# router REST Framework for views registration
router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'customers', CustomerViewSet)

# schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Multi-Tenant API",
        default_version='v1',
        description="API for multi-tenant application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


# list of URLs
urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Endpoint to get token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # Endpoint to refresh token
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('tenants/add/', views.add_tenant, name='add_tenant'),  # Adding tenants
    path('tenants/<uuid:tenant_id>/', views.tenant_detail, name='tenant_detail'),  # Widok dashboard
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/<uuid:tenant_id>/add_organization/', views.add_organization, name='add_organization'),
    path('organizations/<int:organization_id>/', views.organization_detail, name='organization_detail'),
    path('organizations/<int:organization_id>/edit/', views.edit_organization, name='edit_organization'),
    path('organizations/<int:organization_id>/delete/', views.delete_organization, name='delete_organization'),
    path('organizations/<int:organization_id>/add_department/', views.add_department, name='add_department'),
    path('departments/<int:department_id>/edit/', views.edit_department, name='edit_department'),
    path('departments/<int:department_id>/delete/', views.delete_department, name='delete_department'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),
    path('departments/<int:department_id>/add_customer/', views.add_customer, name='add_customer'),
    path('customers/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    path('customers/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),

]


