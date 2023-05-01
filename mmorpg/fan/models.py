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


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    subscriptions = models.ManyToManyField('Category', blank=True, related_name='users')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='users')
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def str(self):
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

class Meta:
    verbose_name = 'CustomUser'
    verbose_name_plural = 'CustomUsers'


class Advertisement(models.Model):
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
        'AdSubscription',
        related_name='advertisements',
        blank=True,
    )

class AdSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ad_subscriptions')
    category = models.CharField(choices=Advertisement.CATEGORIES, max_length=20)
class Response(models.Model): #определяет ответы на объявления
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.advertisement.title} - {self.user.email} - {self.created_at}'

