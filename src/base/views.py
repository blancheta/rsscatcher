from django.shortcuts import render, redirect, reverse


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return render(request, 'base/index.html')
