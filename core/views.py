from django.shortcuts import render
from rest_framework import viewsets
from core.models import Tenant, Organization, Department, Customer
from core.serializers.tenant import TenantSerializer
from core.serializers.organization import OrganizationSerializer
from core.serializers.department import DepartmentSerializer
from core.serializers.customer import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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