from django import forms
from .models import Campaign,Applicants

class campaign_form(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ('user','status')
class applicant_form(forms.ModelForm):
    class Meta:
        model = Applicants
        fields = ['document']

