from django import forms
from account.models import User

class signinForm(forms.ModelForm):
    name = forms.CharField(label='username', max_length=75, required=True)
    password = forms.CharField(label='pw', max_length=75, required=True)
    email = forms.EmailField(label='email', required=True)
    phonenumber = forms.CharField(label='phonenumber', max_length=11, required=True)
    age = forms.IntegerField(label='age', min_value=0, required=True)
    gender = forms.ChoiceField(label='gender', choices=[('M', 'Male'), ('F', 'Female')], required=True)
    
    class Meta:
        model = User
        fields = ['name', 'password', 'email', 'phonenumber', 'age', 'gender']