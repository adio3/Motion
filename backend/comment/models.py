from django.contrib.auth import get_user_model
from django.db import models

from post.models import Post

User = get_user_model()


class Comment(models.Model):
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(to=User, related_name="comments", on_delete=models.CASCADE, blank=True, null=True)

    post = models.ForeignKey(to=Post, related_name="comments", on_delete=models.CASCADE, blank=True, null=True)
