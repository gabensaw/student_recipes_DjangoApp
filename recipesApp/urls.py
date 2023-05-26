from django.urls import path
from .views import (
    RecipeListView,
    RecipeDetailView,
    FormWizardView,
    UpdateFormWizardView,
    RecipeDeleteView,
    UserRecipeListView, MyRecipeView
)
from . import views
from .forms import *
from django.conf import settings
from django.conf.urls.static import static

FORMS = [
    ('RecipeForm', RecipeForm),
    ('1', IngredientInlineFormset),
    ('NutrientForm', NutrientForm),
]

# urls for recipes application
urlpatterns = [
    path('', RecipeListView.as_view(), name='recipes-home'),
    path('user/<str:username>/', UserRecipeListView.as_view(), name='user-recipes'),
    path('myrecipes/', MyRecipeView.as_view(), name='my-recipes'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/<int:pk>/update/', UpdateFormWizardView.as_view(FORMS), name='recipe-update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe/new/', FormWizardView.as_view(), name='recipe-create'),
    path('about/', views.about, name='recipes-about')
]

# add static and media url root to recipes app urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
