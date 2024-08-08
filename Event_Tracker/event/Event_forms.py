from django import forms
from . import models

from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

class NameForm(forms.Form):
    erorr_css_class = 'error-field'
    required_css_class = 'required-field'
    Event_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Event Name"}),max_length=35)
    Event_location = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Event Location"}),max_length=35)
    Event_Org = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Event Organization"}),max_length=35)
    #Event_host = forms.ForeignKey(models.Event_Users, on_delete=forms.CASCADE)
    Event_start_date = forms.DateTimeField(widget=DateTimePickerInput)
    Event_end_date = forms.DateTimeField(widget=DateTimePickerInput)

class SocialForm(forms.Form):
    twitterSocial = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Twitter"}),max_length=35)
    instagramSocial = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Instagram"}),max_length=35)
    snapSocial = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Snap"}),max_length=35)

