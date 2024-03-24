from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    place = models.CharField(max_length=150,null=True,blank=True)
    district = models.CharField(max_length=150,null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    bio = models.TextField()
    friends_list = models.ManyToManyField('self')
    blocked_list = models.ManyToManyField('self')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
