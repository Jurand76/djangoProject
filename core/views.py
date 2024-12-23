from django.shortcuts import render, redirect
from rest_framework import viewsets
from core.models import Tenant, Organization, Department, Customer
from core.serializers.tenant import TenantSerializer
from core.serializers.organization import OrganizationSerializer
from core.serializers.department import DepartmentSerializer
from core.serializers.customer import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'tenant_id',
            openapi.IN_QUERY,
            description="ID Tenanta (UUID)",
            type=openapi.TYPE_STRING,
        )
    ])

    def get_queryset(self):
        tenant = self.request.tenant
        if tenant is None:
            return Organization.objects.none()
        return Organization.objects.filter(tenant=tenant)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        if tenant is None:
            return Department.objects.none()
        return Department.objects.filter(tenant=tenant)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        if tenant is None:
            return Customer.objects.none()
        return Customer.objects.filter(tenant=tenant)


def homepage(request):
    return render(request, 'core/homepage.html')

@login_required
def tenant_list(request):
    tenants = Tenant.objects.all()  # Here can be filtering added
    return render(request, 'core/tenant_list.html', {'tenants': tenants})


@login_required
def add_tenant(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        if domain:
            Tenant.objects.create(domain=domain)
            return redirect('tenant_list')
    return render(request, 'core/add_tenant.html')

def homepage(request):
    try:
        template = get_template('base.html')
        print(f"Template found: {template}")
    except Exception as e:
        print(f"Error: {e}")
    return render(request, 'core/homepage.html')