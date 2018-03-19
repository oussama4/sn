from django.urls import path

from .views import post_action, index

app_name = 'feed'
urlpatterns = [
    path('feed/post', post_action, name='post_action'),
    path('', index, name='index'),
]