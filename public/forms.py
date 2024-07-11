from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PhotoMissingPeopleForm(forms.ModelForm):
    class Meta:
        fields = ['photo']
        model = MissingPerson
        
class ReportForm(forms.ModelForm):
    class Meta:
        fields = ["status","additional_info",]
        model = ReportInformation
    
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-100 form-control  py-3 my-3 col-6'
            
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'latitude', 'longitude')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_staff = False
        if commit:
            user.save()
            UserProfile.objects.create(user=user, latitude=self.cleaned_data['latitude'], longitude=self.cleaned_data['longitude'])
        return user
    
class FoundPersonDetailsForm(forms.ModelForm):
    class Meta:
        model = FoundPersonDetails
        fields = ['found_date','state', 'current_health_status', 'other_detiles','found_location_lat','found_location_lng']
        widgets = {
            'found_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'current_health_status': forms.TextInput(attrs={'class': 'form-control'}),
            'other_detiles': forms.Textarea(attrs={'class': 'form-control'}),
            'state':forms.TextInput(attrs={'class': 'form-control'}),
        }

    found_location_lat = forms.FloatField(widget=forms.HiddenInput())
    found_location_lng = forms.FloatField(widget=forms.HiddenInput())