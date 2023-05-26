from django.urls import path
from users import views as user_views

# url for delete account
urlpatterns = [
    path('delete-account/', user_views.delAccount, name='deleteAccount'),
]
