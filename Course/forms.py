from django import forms
from django.contrib.auth.models import User

from .models import Comment,profile , work, work_for_competition


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)
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
        fields = ('first_name','last_name','email')
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('bio', 'photo', 'date_of_birth', 'facility',)
class UploadWorkForm(forms.ModelForm):
    class Meta:
        model = work
        fields = ('name', 'work', 'theme',)
# class SingUpForm(forms.Form):
#     work = forms.ModelChoiceField(queryset=work.objects.filter())
#     competition = forms.HiddenInput()
#     def __init__(self, *args, **kwargs):
#         #using kwargs
#         self.request = kwargs.pop("request")
#         super(SingUpForm, self).__init__(*args, **kwargs)
#         self.fields['work'].queryset = work.objects.filter(author=profile.objects.get(user=self.request.user))
#     def save(self):
#         return self.work,self.competition4
class MSingUpForm(forms.ModelForm):
    class Meta:
        model = work_for_competition
        fields = ('work_name',)
        exclude = ('competition',)