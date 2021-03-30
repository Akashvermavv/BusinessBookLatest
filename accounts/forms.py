from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from django_countries import countries




class user_account_form(forms.Form):
    COUNTRIES = tuple(countries)


    first_name=forms.CharField(max_length=25, required=True ,widget=forms.TextInput(attrs={'class':'form-control','id':'firstName','placeholder':'First Name'}))
    last_name=forms.CharField(max_length=25, required=True,widget=forms.TextInput(attrs={'class':'form-control','id':'lastName','placeholder':'Last Name'}))
    email = forms.EmailField(max_length=35, required=True,widget=forms.TextInput(attrs={'class':'form-control','id':'emailAddress','placeholder':'Email'}))
    mobile=PhoneNumberField(max_length=16,required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'mobile','placeholder':'Mobile'}))
    address=forms.CharField(max_length=45, required=True,widget=forms.TextInput(attrs={'class':'form-control','id':'address','placeholder':'Address'}))
    country =forms.ChoiceField(label="Select your country",choices=COUNTRIES,required=True,widget=forms.Select(attrs={'class':'form-control country','id':None}))
    
    company=forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class':'form-control','id':'company','placeholder':'Company'}))
    password=forms.CharField(max_length=15,widget=forms.PasswordInput(attrs={'class':'form-control','id':'password1','placeholder':'Password'}), required=True)
    confirm_password=forms.CharField(max_length=15,widget=forms.PasswordInput(attrs={'class':'form-control','id':'password2','placeholder':'Confirm Password'}), required=True)
