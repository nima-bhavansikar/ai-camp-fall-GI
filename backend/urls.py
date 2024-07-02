from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from sandbox.views import (
    main_sanbox_view,
    course_one_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),

    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('settings/', TemplateView.as_view(template_name='settings.html'), name='settings'),

    #path("python_course/", TemplateView.as_view(template_name="courses/python.html"), name="python_course"),
    #path("course1/", TemplateView.as_view(template_name="courses/course1.html"), name="course1"),
    #path("courses/<str:course_identifier>/", views.load_course, name="course_base"),

    path("community/", include("community.urls", namespace="community")),
    path("sandbox/", include("sandbox.urls", namespace="sandbox")),

]