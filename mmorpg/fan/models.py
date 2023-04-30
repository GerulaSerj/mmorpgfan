from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(Group, blank=True, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="custom_user_user_permissions"
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Category(models.Model): #определяет категории объявлений
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Advertisement (models.Model): #определяет объявления, которые пользователи могут создавать и редактировать
    CATEGORIES = (
        ('TANKS', 'Танки'),
        ('HEALERS', 'Хилы'),
        ('DPS', 'ДД'),
        ('TRADERS', 'Торговцы'),
        ('GUILDMASTERS', 'Гилдмастеры'),
        ('QUESTGIVERS', 'Квестгиверы'),
        ('BLACKSMITHS', 'Кузнецы'),
        ('LEATHERWORKERS', 'Кожевники'),
        ('ALCHEMY', 'Зельевары'),
        ('MAGES', 'Мастера заклинаний'),
    )

    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.CharField(choices=CATEGORIES, max_length=20)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='advertisements')
    created_at = models.DateTimeField(auto_now_add=True)

class Response(models.Model): #определяет ответы на объявления
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.advertisement.title} - {self.user.email} - {self.created_at}'

class Subscription(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )