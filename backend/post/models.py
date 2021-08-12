from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()

    links = models.URLField(blank=True)

    media = models.ImageField(upload_to='post_media', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(to=User, related_name="posts", on_delete=models.CASCADE, blank=True, null=True)

    likes = models.ManyToManyField(to=User, related_name="liked_posts", blank=True)

    # how to do a one to many relationship to the same instance class?
    shared_post = models.ForeignKey(to="self", related_name="shared_in", on_delete=models.CASCADE, blank=True, null=True)