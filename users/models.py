from django.db import models
from django.contrib.auth.models import User


# a model to create a user profile and store it in the database
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # method that returns the object name as the name of the user profile
    def __str__(self):
        return f'{self.user.username} profile'
