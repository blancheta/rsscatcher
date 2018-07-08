from django.shortcuts import render, redirect, reverse
from django.views import View


class HomeView(View):

    """
    Render the home view for visitors
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))
        return render(request, 'base/index.html')
