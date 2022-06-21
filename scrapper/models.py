from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# CustomUser: this model is for making the email field unique for the 
# login page.

class CustomUser (AbstractUser):
    email = models.EmailField('email address', unique=True)