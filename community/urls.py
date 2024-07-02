from django.urls import path
from . import views
from django.urls.converters import UUIDConverter
from django.views.generic.base import TemplateView

app_name = "community"

class UuidConverter(UUIDConverter):
    regex = '[0-9a-f-]+'

urlpatterns = [
    path("", views.list_of_posts, name="list_of_posts"),

    #path("create-post/", TemplateView.as_view(template_name="community/post_form.html"), name="create_post"),
    #path("create/", TemplateView.as_view(template_name="community/create_post.html"), name="create_post"),
    path("create/", views.get_post_form, name="create_url"),
    path("create_post/", views.create_post, name="create_post"), #

    path("<uuid:id>/", views.post_details, name="post_details"), # views function, name of path
    #path("<int:id>/", views.post_details, name="post_details"), # views function, name of path

    path("<uuid:post_id>/comment/", views.comment_for_post, name="comment_for_post"),

    path("upvote/<str:type>/<id>/", views.upvote, name="upvote"),

    path("demo_share/<uuid:id>", views.shared_link, name='demo_share'),
    path("check_notebook_link/", views.check_notebook_link, name="check_notebook_link"),
]

"""

comment_for_post is a model
but its comment_form is also embedded

create_post is a model
but why are we urling it?

^this solved the problem

"""