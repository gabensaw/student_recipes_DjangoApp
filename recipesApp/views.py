from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import (ListView, DetailView, DeleteView)
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from .forms import *

import logging

logger = logging.getLogger('django')


# Home page view passed to template along with all recipes
def home(request):
    context = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'recipes/home.html', context)


# Recipes page view passed to template from latest listing 9 recipes by page
class RecipeListView(ListView):
    model = Recipe
    # template_name and context_object_name is convention in django for templates name and context in class based view
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-dateAdded']

    paginate_by = 9

    # queryset method that sends a query to the database and returns the result of searching or selecting a category
    def get_queryset(self):
        category = self.request.GET.get('c', 'NONE')
        search = self.request.GET.get('s', 'NONE')
        if category != 'NONE':
            return Recipe.objects.filter(recipeCategory=category).order_by('-dateAdded')
        if search != 'NONE':
            return Recipe.objects.filter(recipeName__icontains=search).order_by('-dateAdded')
        return Recipe.objects.all().order_by('-dateAdded')


# Logged-in user recipes page view
class MyRecipeView(ListView):
    model = Recipe
    template_name = 'recipes/my_recipe.html'
    context_object_name = 'recipes'
    paginate_by = 9

    # method that returns all the recipes of the logged user from DB
    def get_queryset(self):
        self.kwargs = {"username": self.request.user.username}
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        logger.info('url:%s method:%s ' % (self.request.path, self.request.method))
        return Recipe.objects.filter(author=user).order_by('-dateAdded')


# all recipes of any selected user - page view
class UserRecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/user_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        logger.info('url:%s method:%s ' % (self.request.path, self.request.method))
        return Recipe.objects.filter(author=user).order_by('-dateAdded')


# Detail view page rendering in template
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'


# A 3-step form for adding a new recipe to the website - page view
class FormWizardView(LoginRequiredMixin, SessionWizardView):
    template_name = "recipes/recipe_form.html"
    form_list = [RecipeForm, IngredientInlineFormset, NutrientForm]
    file_storage = FileSystemStorage(location='/mediafiles/recipes_pics')

    # saving all 3 forms in DB and redirect to new created recipe page
    def done(self, form_list, **kwargs):
        form_list[0].instance.author = self.request.user
        recipeID = (form_list[0].save().id)
        for form in form_list[1]:
            form.instance.recipeName_id = recipeID
            form.save()
        form_list[2].instance.recipeName_id = recipeID
        form_list[2].save()

        logger.info('url:%s method:%s ' % (self.request.path, self.request.method))
        return redirect(reverse_lazy("recipe-detail", kwargs={'pk': recipeID}))


# Update forms information using same 3-step form
class UpdateFormWizardView(LoginRequiredMixin, SessionWizardView):
    template_name = "recipes/recipe_form.html"
    file_storage = FileSystemStorage(location='/mediafiles/recipes_pics')

    def get_form_initial(self, step):
        if 'pk' in self.kwargs:
            return {}
        return self.initial_dict.get(step, {})

    # method that get values from forms created on the new recipe page
    def get_form_instance(self, step):
        if not self.instance_dict:
            if 'pk' in self.kwargs and step == 'RecipeForm':
                pk = self.kwargs['pk']
                return Recipe.objects.get(id=pk)
            elif 'pk' in self.kwargs and step == '1':
                pk = self.kwargs['pk']
                result = Recipe.objects.get(id=pk)
                return result
            elif 'pk' in self.kwargs and step == 'NutrientForm':
                pk = self.kwargs['pk']
                return Nutrient.objects.get(recipeName=pk)
        return self.initial_dict.get(step, None)

    # saving all 3 updated forms in DB and redirect to new created recipe page
    def done(self, form_list, **kwargs):
        form_list[0].instance.author = self.request.user
        recipeID = (form_list[0].save().id)
        for form in form_list[1]:
            form.instance.recipeName_id = recipeID
            form.save()
        form_list[2].instance.recipeName_id = recipeID
        form_list[2].save()

        logger.info('url:%s method:%s ' % (self.request.path, self.request.method))
        return redirect(reverse_lazy("recipe-detail", kwargs={'pk': recipeID}))


# Delete page view - allows the user who created the recipe to delete it
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_message = "This recipe was deleted successfully"

    # method that adds a success message for deleting a recipe on homepage
    def get_success_url(self):
        messages.success(self.request, "The recipe was deleted successfully")
        return reverse('recipes-home')

    # method that checks if the user is the author of the recipe
    def test_func(self):
        recipe = self.get_object()
        logger.info('url:%s method:%s ' % (self.request.path, self.request.method))
        if self.request.user == recipe.author:
            return True
        return False


# About function view
def about(request):
    logger.info('url:%s method:%s ' % (request.path, request.method))
    return render(request, 'recipes/about.html', {'title': 'About'})
