from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone

class Category(models.Model): #определяет категории объявлений
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    subscriptions = models.ManyToManyField(Category, blank=True, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_subscriptions'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_subscriptions'
    )

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
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='advertisement_images/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ads')
    subscriptions = models.ManyToManyField(
        Subscription,
        related_name='ads_subscriptions',
        blank=True,  # делаем поле необязательным
    )

class Response(models.Model): #определяет ответы на объявления
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.advertisement.title} - {self.user.email} - {self.created_at}'

