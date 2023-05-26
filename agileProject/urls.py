"""agileProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

# urls for main application
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('change-password/', auth_views.PasswordResetView.as_view(template_name="users/change-password.html",
                                                                  success_url="/email-sent/"),
         name='changePassword'),
    path('email-sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/email-sent.html"),
         name='emailSent'),
    path('password-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password-confirm.html",
                                                     success_url="/complete-change/"),
         name='password_reset_confirm'),
    path('complete-change/', auth_views.PasswordResetCompleteView.as_view(template_name="users/complete-change.html"),
         name='passwordChanged'),
    path('', include('recipesApp.urls')),
    path('', include('users.urls'))
]

# add static and media url root to main urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
