import random

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# snippet to generate random code
def code_generator(length=5):
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


class Reg_profile(models.Model):
    code = models.CharField(max_length=5, default=code_generator)

    activated = models.BooleanField(default=False)

    action = models.CharField(max_length=100)

    # user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='reg_profile', blank=True, null=True)

    # since the reg_profile is intended work without creating a user before registering we might need an email field here
    email = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'Email: {self.email} - code: {self.code}'
