from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'addressline1', 'addressline2', 'state', 'city', 'phone_number', 'gender', 'dob']


# forms.py
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['username', 'email', 'subject', 'message']
            
            
            
            
from .models import CustomUser  # Assuming CustomUser is your user model

class UpdateCustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Update with your user model
        fields = ['username', 'email', 'phone_number', 'pincode', 'address']




from django import forms

class GoldSampleForm(forms.Form):
    weight = forms.FloatField(label='Weight (grams)')
    volume = forms.FloatField(label='Volume (cubic centimeters)')
    density = forms.FloatField(label='Density (grams per cubic centimeter)')
