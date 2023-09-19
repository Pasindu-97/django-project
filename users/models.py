from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    country = models.CharField("Country", max_length=255)
    telephone = models.CharField("Telephone", max_length=255)
