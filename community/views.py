import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_POST

from .models import Post, Comment, PostManager, SharedLink
from .forms import PostForm, CommentForm

from django.core.exceptions import ValidationError

from sandbox.views import course_names

"""
import pytz
from django.utils import timezone

def convert_to_localtime(utctime):
    fmt = "%m/%d/%Y %H:%M"
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    print(localtz)
    return localtz.strftime(fmt)
"""
def paginate_data(request, data, template_name, per_page=10, extra_context=None):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page")

    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)
    
    context = {"data": paginated_data}
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context)

def list_of_posts(request):
    posts = Post.publishedPosts.all()
    """post_paginator = Paginator(posts, 10)

    posts_page_number = request.GET.get("page")
    posts = post_paginator.get_page(posts_page_number)

    return render(
        request,
        "community/posts.html",
        {"posts": posts},
    )"""
    return paginate_data(request, posts, "community/posts.html")

def get_post_form(request): # gives the form to post
    return render(
        request,
        "community/create_post.html",
        {
            "form": PostForm()
        }
    )

@require_POST
def create_post(request): # add post based on form, need to fix TODO
    #print("request: ", request)
    if not request.user.is_authenticated:
        reponse_data = {
            "success": True,
            "message": "Log in to post",
        }

        return JsonResponse(reponse_data)

    post = None

    print("request.POST:", request.POST)
    
    form = PostForm(data = request.POST)

    #print("here half")

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user

        notebook_link = form.cleaned_data.get("notebook_link")

        if "/demo_share/" in notebook_link:
            parts = notebook_link.split("/demo_share/")

            try:
                shared_link = SharedLink.objects.get(id=parts[1].split("/")[0])
                post.shared_link = shared_link
                print("GOOD xy")
            except Exception as e:
                print("BAD xy", e)
                pass
        
        post.status = "PB"
        post.save()

        # TODO why does post have author_id but comment has author object
        # get the arg for post id to send them to the new post

        #post_details_url = reverse("community:post_details", args=[post_id])
        post_details_url = reverse("community:post_details", args=[post.id])

        print("success")

        return HttpResponseRedirect(post_details_url)
    else:
        form = PostForm(instance=post)
    
    response_data = {
        "success": False,
        "errors": form.errors,
    }
    print("fail")

    return JsonResponse(response_data, status=400)

def post_details(request, id): # give details of a post, including the form
    try:
        post = get_object_or_404(
            Post,
            id=id,
            status=Post.Status.PUBLISHED
        )
        post.request = request

        comments = post.comments.all()#filter(active=True)
        for comment in comments:
            comment.request = request
        """comments_paginator = Paginator(comments, 10)

        comments_page_number = request.GET.get("page")
        comments = comments_paginator.get_page(comments_page_number)
        """
        form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("No post found")
    #print(post.publish)
    #print(convert_to_localtime(post.publish))
    """return render(request, "community/detail.html", {
        "post": post,
        "comments": comments,
        "form": form,

        #"convert_to_localtime": convert_to_localtime,
    })"""
    return paginate_data(
        request,
        comments,
        "community/detail.html",
        extra_context={"post": post, "form": form}
    )

@require_POST
def comment_for_post(request, post_id): # add comment based on form filled
    if not request.user.is_authenticated:
        reponse_data = {
            "success": False,
            "message": "Log in to comment",
        }

        return JsonResponse(reponse_data)

    post = get_object_or_404(Post, id = post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data = request.POST)

    if form.is_valid():
        comment = form.save(commit = False)
        comment.post = post
        comment.author = request.user
        comment.save()

        post_details_url = reverse("community:post_details", args=[post_id])

        return HttpResponseRedirect(post_details_url)
    
    response_data = {
        "success": False,
        "errors": form.errors,
    }

    return JsonResponse(response_data, status=400)

def upvote(request, type, id):
    print("UPVOTE")
    if request.method == "POST":# and request.is_ajax():
        model_type = {
            "comment": Comment,
            "post": Post,
        }[type]

        obj = get_object_or_404(model_type, id=id)
        user_id = request.user.id

        upvoted_user_ids = json.loads(obj.upvoted_user_ids) if obj.upvoted_user_ids else []
        upvoted = user_id in upvoted_user_ids

        if not upvoted:
            upvoted_user_ids.append(user_id)
            obj.upvotes += 1
        else:
            upvoted_user_ids.remove(user_id)
            obj.upvotes -= 1

        obj.upvoted_user_ids = json.dumps(upvoted_user_ids)
        obj.save()

        return JsonResponse({"upvotes": obj.upvotes, "upvoted": not upvoted})

    return JsonResponse({"error": "Invalid request"})

"""

def upvote_comment(request, type, comment_id):
    if request.method == "POST":# and request.is_ajax():
        model_type = {
            "comment": Comment,
            "post": Post,
        }[type]

        obj = get_object_or_404(model_type, id=comment_id)
        user_id = request.user.id

        upvoted_user_ids = json.loads(obj.upvoted_user_ids) if upvoted_user_ids else []
        upvoted = user_id in upvoted_user_ids

        if not upvoted:
            upvoted_user_ids.append(user_id)
            obj.upvotes += 1
        else:
            upvoted_user_ids.remove(user_id)
            obj.upvotes -= 1

        obj.upvoted_user_ids = json.dumps(upvoted_user_ids)
        obj.save()

        return JsonResponse({"upvotes": obj.upvotes, "upvoted": not upvoted})

    return JsonResponse({"error": "Invalid request"})


"""

def shared_link(request, id):
    obj = get_object_or_404(SharedLink, id=id)

    return render(request, "shared_link.html", {
        "shared_link": obj,
        "name": course_names[obj.course_number]
    })

def check_notebook_link(request):
    if request.method == "POST":
        notebook_id = request.POST.get("notebook_id")

        try:
            shared_link = get_object_or_404(SharedLink, id=notebook_id)
            return JsonResponse({"isValid": True})
        except Exception:
            pass
    
    return JsonResponse({"isValid": False})
