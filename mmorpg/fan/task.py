from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Advertisement, Subscription, Category
from datetime import datetime, timedelta
from django.template.loader import render_to_string



@receiver(advertisement_save, sender=Advertisement)
def product_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Новое объявление в категории {instance.category}'

    text_content = (
        f'Заголовок: {instance.name}\n'
        f'Ссылка на объявление: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Заголовок: {instance.name}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@receiver(advertisement_save, sender=Advertisement)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.__class__.__name__ == 'Advertisement':
        product_created.apply_async(
            (instance.id, instance.title, instance.text),
            countdown=10,
        )
