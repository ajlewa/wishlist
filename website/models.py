from typing import Iterable
from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from random import randrange
from website.helpers import RandomFileName
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_image = models.ImageField(default='default.png', upload_to=RandomFileName('profile_images'))

    following = models.ManyToManyField('self', symmetrical=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

@receiver(post_save, sender=User)
def category_create(sender, instance=None, created=False, **kwargs):
    if created:
        Category.objects.create(name = "Без Категории", color = f'{randrange(255):x}{randrange(255):x}{randrange(255):x}', owner = instance)

class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    color = ColorField(default='#FF0000', format='hex')

    class Meta():
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

class Wish(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    categories = models.ManyToManyField(Category)
    reserved = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    link = models.URLField(default=None, blank=True)
    wish_image = models.ImageField(default='default_wish.png', upload_to=RandomFileName('wish_images'))

    class Meta():
        verbose_name_plural = "Wishes"
    
    def __str__(self):
        return f"{self.name}"
    
class WishReservation(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.wish.name} reserved by {self.user.username}"