from django.urls import path
from .views import PostListView

urlpatterns = [
    # path('', post_view, name='post_url'),
    path('', PostListView.as_view(), name='post_url'),
]
