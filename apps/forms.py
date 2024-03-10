from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from apps.models import User, Order


class UserRegistrationForm(forms.ModelForm):
    # first_name = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(label='Password', required=True)
    password_confirm = forms.CharField(label='Confirm Password', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'quantity', 'phone_number', 'product')


class UserSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'intro')
