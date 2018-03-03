from django.urls import path

from .views import post_action

urlpatterns = [
    path('feed/post', post_action, name='post_action'),
]