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
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('dashboard/<str:tenant_id>/', views.tenant_dashboard, name='tenant_dashboard'),  # Widok dashboard
    path('tenants/add/', views.add_tenant, name='add_tenant'),  # Adding tenants
]


