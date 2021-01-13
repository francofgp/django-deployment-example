from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo


# lo que hago aca es creo el form para el usuario
# que tiene sus atributos por defecto
# luego a esto le agregue otro FORM con los atributos que le agregue
# a mi usuario
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
