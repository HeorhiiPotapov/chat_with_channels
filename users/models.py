from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    name = models.CharField('username', max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="uploads/profile_images/%Y/%m/%d",
        default='default/profile.jpg')

    class Meta:
        verbose_name_plural = 'Profile'

    def __str__(self):
        return str(self.user.name)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.user.pk})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
