from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# method that automatically creates a user profile after submitting valid data from the new user registration form
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# method that automatically saves the user profile after it has been created by the create_profile signal
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
