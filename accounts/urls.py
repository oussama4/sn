from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUp, profile, follow

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='index.html'),
        name='logout'),
    path('register', SignUp.as_view(), name='signup'),
    path('follow_user', follow, name='follow_user'),
    path('profile/<int:pk>/', profile, name='profile'),
]