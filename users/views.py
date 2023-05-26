from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.contrib import messages

import logging

logger = logging.getLogger('django')


# Register create views function
def register(request):
    # post request contains user post request
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # check that user creation form is valid from post request
        if form.is_valid():
            # save user form with hashed password
            form.save()
            username = form.cleaned_data.get('username')
            # flash message shows received valid data - one-time alert
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    logger.info('url:%s method:%s ' % (request.path, request.method))
    return render(request, 'users/register.html', {'form': form})


# Profile page view with update profile functionality - login_required decorator that checks if user is logged in
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    # if POST request fails, display previous valid user data
    else:
        u_form = UserUpdateForm(instance=request.user, initial={'username': request.user.username})

    context = {
        'u_form': u_form,
    }
    logger.info('url:%s method:%s ' % (request.path, request.method))
    return render(request, 'users/profile.html', context)


# Delete view function to delete the account of a logged in user
@login_required
def delAccount(request):
    if request.method == 'POST':
        print("test")
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, f'Your account has been deleted!')
        return redirect('login')
    logger.info('url:%s method:%s ' % (request.path, request.method))
    return render(request, 'users/delete-account.html')
