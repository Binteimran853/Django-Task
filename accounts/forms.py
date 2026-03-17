from django import forms
from .models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_image', 'address', 'phone']
        labels = {
            'Username' : 'username',
            'Email' : 'email',
            'Password' : 'password',
            'Profile image' : 'profile_image',
            'Address' : 'address',
            'Phone Number' : 'phone',
        }


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if (User.objects.filter(username=username).exists() or
                User.objects.filter(email=email).exists()):
            raise ValidationError("Email or username already registered")
        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model : User
        fields = ['username', 'email', 'profile_image', 'address', 'phone']
        # labels = {
        #     'Username' : 'username',
        #     'Email' : 'email',
        #     'Profile image' : 'profile_image',
        #     'Address' : 'address',
        #     'Phone Number' : 'phone',
        # }