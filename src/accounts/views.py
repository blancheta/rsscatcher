from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegistrationForm


def signup(request):

    """
        Signup view
    """

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user if form valid
            User.objects.create_user(
                form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )

            messages.success(request, 'Your account has been created')
            return redirect(reverse('accounts_login'))
    else:
        form = RegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})
