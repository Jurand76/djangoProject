from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from core.models import Tenant, Organization, Department, Customer
from core.serializers.tenant import TenantSerializer
from core.serializers.organization import OrganizationSerializer
from core.serializers.department import DepartmentSerializer
from core.serializers.customer import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required
from core.forms import OrganizationForm, CustomerForm, DepartmentForm


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
            description="ID of tenant (UUID)",
            type=openapi.TYPE_STRING,
        )
    ])
    def get_queryset(self):
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            return Organization.objects.filter(tenant__tenant_id=tenant_id)

        tenant = self.request.tenant
        if tenant is None:
            return Organization.objects.none()
        return Organization.objects.filter(tenant=tenant)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        tenant_id = self.request.query_params.get('tenant_id')
        organization_id = self.request.query_params.get('organization_id')
        if tenant_id and organization_id:
            return Department.objects.filter(organization__tenant__tenant_id=tenant_id, organization_id=organization_id)

        tenant = self.request.tenant
        if tenant is None:
            return Department.objects.none()
        return Department.objects.filter(tenant=tenant)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        tenant_id = self.request.query_params.get('tenant_id')
        organization_id = self.request.query_params.get('organization_id')
        department_id = self.request.query_params.get('department_id')
        if tenant_id and organization_id and department_id:
            return Customer.objects.filter(department__organization__tenant__tenant_id=tenant_id,
                                           department__organization_id=organization_id,
                                           department_id=department_id)

        tenant = self.request.tenant
        if tenant is None:
            return Customer.objects.none()
        return Customer.objects.filter(tenant=tenant)


def homepage(request):
    tenants = Tenant.objects.all()  # Get all tenants
    is_admin = request.user.is_authenticated and request.user.is_staff  # Check if user has admin privileges
    return render(request, 'core/homepage.html', {
        'tenants': tenants,
        'is_admin': is_admin,
    })


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


def tenant_detail(request, tenant_id):
    # Get tenant
    tenant = get_object_or_404(Tenant, tenant_id=tenant_id)
    # Get organizations
    organizations = Organization.objects.filter(tenant=tenant)

    return render(request, 'core/tenant_detail.html', {
        'tenant': tenant,
        'organizations': organizations,
    })


def organization_detail(request, organization_id):
    # Get organization
    organization = get_object_or_404(Organization, id=organization_id)
    # Get departments for organization
    departments = organization.departments.all()
    return render(request, 'core/organization_detail.html', {
        'organization': organization,
        'departments': departments,
    })


def add_organization(request, tenant_id):
    # Get tenant based at tenant_id
    tenant = get_object_or_404(Tenant, tenant_id=tenant_id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.tenant = tenant  # Join organization with tenant
            organization.save()
            return redirect('tenant_detail', tenant_id=tenant.tenant_id)
    else:
        form = OrganizationForm()
    return render(request, 'core/add_organization.html', {'form': form, 'tenant': tenant})


def edit_organization(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('tenant_detail', tenant_id=organization.tenant.tenant_id)
    else:
        form = OrganizationForm(instance=organization)
    return render(request, 'core/edit_organization.html', {'form': form, 'organization': organization})


def delete_organization(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    if request.method == 'POST':
        tenant_id = organization.tenant.tenant_id
        organization.delete()
        return redirect('tenant_detail', tenant_id=tenant_id)
    return render(request, 'core/delete_organization.html', {'organization': organization})


def department_detail(request, department_id):
    # Get department
    department = get_object_or_404(Department, id=department_id)
    # Get customers list
    customers = department.customers.all()
    return render(request, 'core/department_detail.html', {
        'department': department,
        'customers': customers,
    })


def add_department(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.organization = organization  # Join department with organization
            department.save()
            return redirect('organization_detail', organization_id=organization.id)
    else:
        form = DepartmentForm()
    return render(request, 'core/add_department.html', {'form': form, 'organization': organization})


def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('organization_detail', organization_id=department.organization.id)
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'core/edit_department.html', {'form': form, 'department': department})


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        organization_id = department.organization.id
        department.delete()
        return redirect('organization_detail', organization_id=organization_id)
    return render(request, 'core/delete_department.html', {'department': department})


def add_customer(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.department = department
            customer.save()
            return redirect('department_detail', department_id=department.id)
    else:
        form = CustomerForm()
    return render(request, 'core/add_customer.html', {'form': form, 'department': department})


def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('department_detail', department_id=customer.department.id)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'core/edit_customer.html', {'form': form, 'customer': customer})


def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        department_id = customer.department.id
        customer.delete()
        return redirect('department_detail', department_id=department_id)
    return render(request, 'core/delete_customer.html', {'customer': customer})
