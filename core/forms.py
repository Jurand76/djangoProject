from django import forms
from core.models import Organization, Customer, Department

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']  # Organization name

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']  # Customer name and email

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']           # Deparment name
