from django.urls import path

from .views import post_action, index, SearchView

app_name = 'feed'
urlpatterns = [
    path('feed/post', post_action, name='post_action'),
    path('search', SearchView.as_view(), name='search'),
    path('', index, name='index'),
]