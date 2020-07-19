from django import forms
from .models import Admin_Profile

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin_Profile
        exclude = ['created', 'this_user']