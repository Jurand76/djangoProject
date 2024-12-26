from django import forms
from core.models import Organization, Customer

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']  # Organization name

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']  # Pola, które użytkownik może edytować
