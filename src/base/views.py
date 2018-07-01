from django.shortcuts import render, redirect, reverse


def home(request):

    """
    Render the home view for visitors
    """

    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return render(request, 'base/index.html')
