from django.urls import path

from .views import CreatePsotView, index

app_name = 'feed'
urlpatterns = [
    path('feed/post', CreatePsotView.as_view(), name='post_action'),
    path('', index, name='index'),
]