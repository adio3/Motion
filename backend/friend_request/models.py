from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class FriendRequest(models.Model):
    status = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    receiver = models.ForeignKey(to=User, related_name="received_friend_requests", on_delete=models.CASCADE, blank=True,
                                 null=True)

    sender = models.ForeignKey(to=User, related_name="sent_friend_requests", on_delete=models.CASCADE, blank=True,
                               null=True)

    class Meta:
        unique_together = ("sender", "receiver")