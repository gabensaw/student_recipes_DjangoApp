from django.contrib import admin
from .models import Profile

# Register user profile on admin page
admin.site.register(Profile)