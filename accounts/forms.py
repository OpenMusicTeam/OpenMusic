from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('age', 'desc', 'avatar')
        widgets = {
            'age': forms.TextInput(attrs=
            {
                'id': 'age',
                'class': 'form-control'
            }),
            'desc': forms.TextInput(attrs=
            {
                'id': 'desctiption',
                'class': 'form-control',
            }),
            'avatar': forms.FileInput(attrs=
            {
                'id': 'validatedCustomFile',
                'class': 'custom-file-input'
            }),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        new_user = User.objects.create_user(self.cleaned_data['username'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password'])
        # new_user.first_name = self.cleaned_data['first_name']
        # new_user.last_name = self.cleaned_data['last_name']
        if commit:
            new_user.save()
        return new_user
