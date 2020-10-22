from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES =( 
    ("student", "student"), 
    ("teacher", "teacher"),
)

class User(AbstractUser):
    UserField = models.CharField(max_length=20,choices = CHOICES ,blank=False)
    