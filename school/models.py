from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('employee', 'Employee'),
        ('employer', 'Employer'),
    )
    user_type = models.CharField(max_length=8, choices=USER_TYPES)

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user',
    )

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_user_groups',
        related_query_name='custom_user',
    )

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=1)
    company_name = models.CharField(max_length=255, default='test')

class MailDetails(models.Model):
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=128)

class Email(models.Model):
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)