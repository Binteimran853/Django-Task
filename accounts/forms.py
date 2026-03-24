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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
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
        model = User
        fields = ['username', 'email', 'profile_image', 'address', 'phone']

        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'd-none'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        user_id = self.instance.id

        if User.objects.exclude(id=user_id).filter(username=username).exists():
            raise ValidationError("Username already taken")

        if User.objects.exclude(id=user_id).filter(email=email).exists():
            raise ValidationError("Email already registered")

        return cleaned_data