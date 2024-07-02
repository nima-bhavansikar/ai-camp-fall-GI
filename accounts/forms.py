from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
#, SecurityQuestion

class SignUpForm(UserCreationForm):
    security_question = forms.CharField(initial='Mother\'s maiden name')
    #security_question.clean('Mother\'s maiden name:')
    security_answer = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'security_question', 'security_answer')