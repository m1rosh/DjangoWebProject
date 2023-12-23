from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Answer, Question


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=3, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']

        if password != password_repeat:
            raise ValidationError('Passwords mismatch!')

    def save(self):
        self.cleaned_data.pop('password_repeat')
        return User.objects.create_user(**self.cleaned_data)

class ProfileRegisterForm(forms.ModelForm):
    email = forms.CharField(max_length=256, widget=forms.EmailInput(attrs={'class':'form-control'}))
    nickname = forms.CharField(min_length=3, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ['email', 'nickname']

class ProfileSettingForm(forms.Form):
    username = forms.CharField(min_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=256, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(min_length=3, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class AnswerForm(forms.ModelForm):
    content = forms.CharField(min_length=1, widget=forms.Textarea(attrs={'class': 'form-control'}), label='')

    class Meta:
        model = Answer
        fields = ['content']

class QuestionForm(forms.ModelForm):
    title = forms.CharField(min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(min_length=1, widget=forms.Textarea(attrs={'class': 'form-control'}), label='Question text')
    tag = forms.CharField(min_length=1, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter tags separated by space'}))

    class Meta:
        model = Question
        fields = ['title', 'content', 'tag']
