from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=25)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        clean_data = super().clean()
        username = clean_data.get("username")
        password = clean_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль")
            clean_data["user"] = user
        return clean_data