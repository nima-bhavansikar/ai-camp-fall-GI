from collections.abc import Mapping
from typing import Any
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Post, Comment, SharedLink
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
"""
def validate_notebook_link(notebook_link):
    print("in validate_notebook_link")

    if "/demo_share/" not in notebook_link:
        raise ValidationError("Invalid notebook link format.")
    
    parts = notebook_link.split("/demo_share/")

    try:
        shared_link = SharedLink.objects.get(id=parts[1].split("/")[0])
    except SharedLink.DoesNoteExist:
        raise ValidationError("No corresponding notebook ID found for the given link.")
"""
class PostForm(forms.ModelForm):
    notebook_link = forms.URLField(
        required=False,
        label="Notebook Link (optional)",
        #validators=[validate_notebook_link]
    )

    class Meta:
        model = Post
        fields = ["title", "body", "notebook_link"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Title",
                    "class": "form-control",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Body (supports Markdown)",
                    "class": "form-control resizable",
                }
            ),
            
        }
    """
    def clean(self):
        cleaned_data = super().clean()

        validate_notebook_link(cleaned_data.get("notebook_link"))

        return cleaned_data
    """

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Body (supports Markdown)",
                    "class": "form-control resizable",
                    "rows": 5,
                }
            )
        }
