from django import forms
from .models import Admin_Profile, Neighbourhood, Facility, Business

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin_Profile
        exclude = ['created', 'this_user']


class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ['created', 'admin', 'occupants_count']


class AddResidentForm(forms.Form):
    name = forms.CharField(label='Resident name', max_length=50)
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField()    

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        exclude = ['created', 'hood']