import random
import string

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Permission


def random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=30))


# Create your models here.
class Bot(models.Model):
    name = models.fields.CharField(max_length=30, default="Noname")
    status = models.fields.CharField(max_length=30, null=True)
    last_update = models.FloatField()

    def get_dict(self, *args):
        dct = {}
        for arg in args:
            try:
                dct[arg] = getattr(self, arg)
            except Exception:
                pass
        return dct

    def __str__(self):
        return f'{self.name}'


class Token(models.Model):
    name = models.CharField(max_length=30, default=random_string)
    bots = models.ManyToManyField(Bot, blank=True, help_text=(
        "Bots edit field."), )
    service = models.CharField(max_length=100, default="")
    is_supertoken = models.BooleanField(
        "supertoken status",
        default=False,
        help_text=(
            "Designates that this token has all permissions without "
            "explicitly assigning them."
        ),
    )

    def __str__(self):
        return self.service


class Task(models.Model):
    name = models.CharField(max_length=30)
    to_bot = models.ForeignKey(Bot, on_delete=models.CASCADE, blank=True, null=True)
    to_token = models.ForeignKey(Token, on_delete=models.CASCADE, blank=True, null=True)
    sended = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def get_dict(self):
        return {'name': self.name, 'to_bot': self.to_bot.name}

    def __str__(self):
        return f"{self.name}"



class CustomUser(AbstractUser):
    pass
    bots = models.ManyToManyField(Bot, blank=True, help_text=(
        "Bots edit field."))

    def __str__(self):
        return self.username
