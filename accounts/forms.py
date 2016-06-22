from django import forms
from django.contrib.auth.models import User
from Course.models import profile
from django.utils.translation import gettext_lazy as _
class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password') ,widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat password') ,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  ('first_name','last_name','email')
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('bio', 'photo', 'date_of_birth', 'facility')