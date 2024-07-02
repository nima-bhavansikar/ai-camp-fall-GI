from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import signup, email_change, show_email_change_form, username_change, show_username_change_form, password_reset_form, password_reset_form2, password_reset_done, toggle_dark_mode, get_dark_mode


urlpatterns = [
    path("signup/", signup, name="signup"),

    #path("increase_score/", increase_score, name="increase_score"),

    path("username_change/", username_change, name="username_change"),

    path("email_change/", email_change, name="email_change"),

    path('password_reset1/', password_reset_form, name='password_reset1'),

    path('password_reset2/', password_reset_form2, name='password_reset2'),

    path('password_reset3/', password_reset_done, name='password_reset3'),
 
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users_hub/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users_hub/password_reset_complete.html'), name='password_reset_complete'),

    path("toggle-dark-mode/", toggle_dark_mode, name="toggle-dark-mode"),
    path("get-dark-mode/", get_dark_mode, name='get-dark-mode')
]