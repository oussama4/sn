from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .views import SignUp, profile, follow, UpdateUser

app_name = 'accounts'
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='index.html'),
        name='logout'),
    path('register', SignUp.as_view(), name='signup'),
    path('settings/<int:pk>/passwords/', 
        PasswordChangeView.as_view(template_name='accounts/settings.html',
                                    success_url='done',
                                    extra_context={
                                        'gactive': '',
                                        'pactive': 'active',
                                        'is_general': False,
                                        'is_password': True
                                    }), name='change_password'),
    path('settings/<int:pk>/passwords/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_changed.html'),
        name='password_change_done'),
    path('settings/<int:pk>/', UpdateUser.as_view(extra_context={
                                                    'gactive': 'active',
                                                    'pactive': '',
                                                    'is_general': True,
                                                    'is_password': False
                                                }), name='update_user'),
    path('follow_user', follow, name='follow_user'),
    path('profile/<int:pk>/', profile, name='profile'),
]