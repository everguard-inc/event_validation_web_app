from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Redefined default Django UserModel. To be more flexible in further editing.
    """
    pass
