from django.urls import path
from .views import (
tweet_list_view, tweet_detail_view, tweet_profile_view) 

urlpatterns = [
    path('<int:tweet_id>', tweet_detail_view),
    path('', tweet_list_view),
    # path('profile/<str:username>', tweet_profile_view)
]
