from django import forms
from .models import Admin_Profile, Neighbourhood

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin_Profile
        exclude = ['created', 'this_user']


class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ['created', 'admin', 'occupants_count']