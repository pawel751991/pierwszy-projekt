from django import forms
from django.contrib.auth.models import User

from sklint.models import Order, Client


class CheckoutForm(forms.ModelForm):
    ordered_by = forms.CharField(max_length=200, label='Zamawiający')
    address = forms.CharField(max_length=200, label='Adres dostawy')
    mobile = forms.CharField(max_length=12, label='Numer telefonu')

    class Meta:
        model = Order
        fields = ["ordered_by", "address", "mobile", "email"]


class ClientRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Client
        fields = ['username', 'password', 'email']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Użytkownik o podanej nazwie użytkownika już istnieje!")

        return username


class ClientLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')