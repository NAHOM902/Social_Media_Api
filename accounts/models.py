from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# class CustomUser(models.Model):
#     profile_picture = models.ImageField('profile_pics/', blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)


class CustomUserManager(BaseUserManager):

    def creat_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("email must be provided!!"))
        email = self.normalize_email(email)

        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save()


        return new_user
    

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("superuser should have is_stuf as True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("superuser should have is_superuser as True"))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_("superuser should have is_active as True"))
        
        return self.creat_user(email, password, **extra_fields)
    


class User(AbstractUser):

    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=80, unique=True)
    phone_number = PhoneNumberField(null=False, unique=True)
    bio = models.TextField(max_length=100, blank=True)
    profile_picture = models.URLField(blank=True)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']


    objects = CustomUserManager()


    def __str__(self):
        return f"<user {self.email}>"
    



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"posted by {self.author.username} - {self.timestamp}"