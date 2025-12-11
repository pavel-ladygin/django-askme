from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile

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
    

class SingupForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Введите email'})
    )
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    

class EditProfileForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',max_length=25)

    email = forms.EmailField(label='Email')

    nickname = forms.CharField( label='Отображаемое имя', max_length=25,required=False)
    bio = forms.CharField(label='О себе',required=False)
    avatar = forms.ImageField(label='Новый аватар',required=False)
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.user = user
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email
        
        if hasattr(user, 'profile'):
            self.fields['nickname'].initial = user.profile.nickname
            self.fields['bio'].initial = getattr(user.profile, 'bio', '')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def save(self):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.save()
        
        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.nickname = self.cleaned_data.get('nickname', '')
        
        if hasattr(profile, 'bio'):
            profile.bio = self.cleaned_data.get('bio', '')
        
        if self.cleaned_data.get('avatar'):
            profile.avatar = self.cleaned_data['avatar']
        
        profile.save()
        
        return self.user
