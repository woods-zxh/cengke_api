from django.db import models
from django.contrib.auth.models import AbstractUser


class Nuser(AbstractUser):
    sigh = models.CharField(max_length=100,default="I am goo!")


