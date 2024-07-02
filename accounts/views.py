from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views import generic
#from django.contrib.auth.models import User
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from .models import SecurityQuestion
from accounts.models import CustomUser

#security_question_object = SecurityQuestion.objects.create(question='Mother\'s maiden name')
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import UserData

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #print(request.user.security_question)
        #print(form.password1)
        #print(form.password2)
        #print(form.security_answer)
        print("Test")
        print(request.POST.get('security_answer'))
        print(request.POST.get('security_question'))
        
        if form.is_valid():
            print("Form is Valid")
            data = request.POST
            print(request.POST.get('security_answer'))
            print(request.POST.get('security_question'))
            user = form.save()
            user.save() 
            login(request, user)
            return render(request, "home.html", {'form':form})
        #else:
        #    print("Form is invalid")
        #    return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {'form':form})

'''
class CustomUCF(UserCreationForm):
    email = forms.EmailField(
        required=True,
        #widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
        self.fields["username"].widget.attrs.update({'class' : 'form-control'})
        self.fields["email"].widget.attrs.update({'class' : 'form-control'})
        self.fields["password1"].widget.attrs.update({'class' : 'form-control'})
        self.fields["password2"].widget.attrs.update({'class' : 'form-control'})

class SignUpView(generic.CreateView):
    form_class = CustomUCF
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
'''

"""
def increase_score(request):
    if request.user.is_authenticated:
        user_data = request.user.userdata
        user_data.score += 1
        user_data.save()
    return redirect("home")
"""

@login_required
@require_POST
def toggle_dark_mode(request):
    # added .id to this and line 51 according to StackOverflow
    user_data = UserData.objects.get(user=request.user.id)
    
    user_data.darkmode = not user_data.darkmode
    user_data.save()

    return JsonResponse({"dark_mode": user_data.darkmode})

@login_required
def get_dark_mode(request):
    user_data = UserData.objects.get(user=request.user.id)
    return JsonResponse({"dark_mode": user_data.darkmode})

"""
class PythonCourseView(generic.CreateView):
    template_name = "courses/course1.html"
"""


class ChangeEmailForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the 
    e-mail.
    """
    error_messages = {
        'email_mismatch': ("The two email addresses fields didn't match."),
        'not_changed': ("The email addresses are either mismatched OR the same as the one already defined."),
    }

    new_email1 = forms.EmailField(
        label=("New email address"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=("New email address confirmation"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        self.is_valid()
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
    
        
        print(str(old_email + "-> " + str(new_email1)))
        
        return new_email1
        

def email_change(request):
    form = ChangeEmailForm(request.user)
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ChangeEmailForm(request.user, request.POST)
            new_email = form.clean_new_email1()
            u = CustomUser.objects.get(username__exact=request.user)
            u.email = new_email
            u.save()
            print("updated the email to " + str(new_email))
            return redirect('home')
        else:
            print(request.method)
            return render(request, "usermgmt/change_email.html", {'form':form})



def show_email_change_form(request) :
    print(request.method)
    return render(request, "usermgmt/change_email.html", {'form':form})


class ChangeUsernameForm(forms.Form):
    error_messages = {
        'mismatch': ("The two username fields didn't match."),
        'not_changed': ("The username is the same as the one already defined."),
    }

    new_username1 = forms.CharField(label=("New username"))

    new_username2 = forms.CharField(label=("New username confirmation"))


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)

    def clean_new_username1(self):
        self.is_valid()
        old_username = self.user.username
        new_username1 = self.cleaned_data.get('new_username1')
        new_username2 = self.cleaned_data.get('new_username1')
        print(str(old_username + "-> " + str(new_username1)))
    
        return new_username1
        

def username_change(request):
    
    form = ChangeUsernameForm(request.user)
    if request.user.is_authenticated:
        print(request.user.username)
        if request.method=='POST':
            form = ChangeUsernameForm(request.user, request.POST)
            new_username = form.clean_new_username1()
            u = CustomUser.objects.get(username__exact=request.user)
            u.username = new_username
            u.save()
            print("updated the username to " + str(new_username))
            return redirect('home')
        else:
            print(request.method)
            return render(request, "usermgmt/change_username.html", {'form':form})



def show_username_change_form(request) :
    print(request.method)
    return render(request, "usermgmt/change_username.html", {'form':form})


class CustomPasswordChangeForm(PasswordChangeForm):
    security_answer = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean_security_answer(self):
        security_answer = self.cleaned_data.get('security_answer')
        if not self.user.security_question.answer == security_answer:
            raise forms.ValidationError('Invalid security answer.')
        return security_answer

def password_reset_form(request) :
    return render(request, 'registration/password_reset_form.html')

def password_reset_form2(request) :
    print('from form2 ')
    return render(request, 'registration/password_reset_form2.html')

def password_reset_done(request) :
    data = request.POST
    print(data.get('password1'))
    print(data.get('password2'))
    if data.get('password1') != data.get('password2') :
        print('from done')
        return render(request, 'registration/password_reset_form2.html')
    u = CustomUser.objects.get(username__exact=data.get('username'))
    if (u.security_answer != data.get('secret')) :
        print('mismatch')
        return render(request, 'registration/password_reset_form2.html')
    else :
        u.set_password(data.get('password1'))
        u.save()
        login(request, u)
        return redirect('home')  # Redirect to the home page or another appropriate URL

  


