from typing import Any
from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import F, Func, F, ExpressionWrapper, Value
from django.db.models import Case, When#Value, Greatest
from django.db.models import DateTimeField, IntegerField, DurationField, FloatField
from accounts.models import CustomUser

from django.utils import timezone

from datetime import datetime
#from datetime import timezone as dttz
import uuid
import json
import math

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        PRIVATE = "PV", "Draft"
        PUBLISHED = "PB", "Published"
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=250)
    #slug = models.SlugField(max_length=250)
    body = models.TextField()

    shared_link = models.ForeignKey(
        "community.SharedLink",
        on_delete=models.CASCADE,
        related_name="post_shared_link",
        null=True,
    )

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    upvotes = models.IntegerField(default=0)
    upvoted_user_ids = models.TextField(default="[]")

    @property
    def upvoted_by_user(self):
        user_id = getattr(self, 'request', None).user.id
        #print(self.upvoted_user_ids)
        upvoted_user_ids = json.loads(self.upvoted_user_ids)
        #print("-")
        #print(user_id in upvoted_user_ids)
        #print("\\\\")
        return user_id in upvoted_user_ids
    
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PRIVATE
    )

    objects = models.Manager()
    publishedPosts = PostManager()

    class Meta:        
        ordering = [
            - (
                F('upvotes') + 1
            ) / (
                (
                    ExpressionWrapper(
                        datetime.now(timezone.utc) - F('publish'),
                        output_field=IntegerField()
                    ) / 86400000000 + 1
                ) ** 3
            ),
            #"-x_ord",
            "-publish"
        ]
        """indexes = [
            models.Index(fields=["-publish", "upvotes"]),
        ]"""

    def __str__(self):
        return f"Post {self.title} by  {self.author}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    #name = models.CharField(max_length=100)
    #email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #active = models.BooleanField(default=True)
    upvotes = models.IntegerField(default=0)
    upvoted_user_ids = models.TextField(default="[]")

    @property
    def upvoted_by_user(self):
        user_id = getattr(self, 'request', None).user.id
        #print(self.upvoted_user_ids)
        upvoted_user_ids = json.loads(self.upvoted_user_ids)
        #print("-")
        #print(user_id in upvoted_user_ids)
        #print("\\\\")
        return user_id in upvoted_user_ids

    class Meta:
        ordering = ["-upvotes", "created"]
        indexes = [
            models.Index(fields=["-upvotes", "created"]),
        ]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}: {self.body} with {self.upvotes} upvotes"

class SharedLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shared_link_author",
        null=True
    )
    
    course_number = models.IntegerField(default=0)

    code = models.TextField(default="{}")

    objects = models.Manager()