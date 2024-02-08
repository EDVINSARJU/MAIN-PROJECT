from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'addressline1', 'addressline2', 'state', 'city', 'phone_number', 'gender', 'dob']
