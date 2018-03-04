from django.urls import path

from .views import post_action, index

urlpatterns = [
    path('feed/post', post_action, name='post_action'),
    path('', index, name='index'),
]