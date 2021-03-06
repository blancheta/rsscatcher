from django.contrib.auth import views as auth_views
from django.urls import path
from .views import signup

urlpatterns = [
    path('signup/', signup, name="accounts_signup"),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True
    ), name="accounts_login"),
    path('logout/', auth_views.LogoutView.as_view(
        next_page="/"
    ), name="accounts_logout")
]
