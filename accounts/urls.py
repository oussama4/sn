from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUp, index, profile

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='index.html'),
        name='logout'),
    path('register', SignUp.as_view(), name='signup'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('', index, name='index')
]